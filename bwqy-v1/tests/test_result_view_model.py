from __future__ import annotations

import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from item_query_v1.result_view_model import CandidateResultModel, ItemResultPageModel, build_result_view_model
from item_query_v1.types import ItemQueryResult, RawRecord, TraceValue


def _item_record(values: dict[str, str]) -> RawRecord:
    return RawRecord(
        table="ItemTable",
        values={
            key: TraceValue(
                source_table="ItemTable",
                source_field=key,
                raw_value=value,
                status="direct",
            )
            for key, value in values.items()
        },
    )


class ResultViewModelTests(unittest.TestCase):
    def test_single_match_builds_item_result_page_model(self) -> None:
        item = _item_record(
            {
                "TID": "100",
                "LocalName": "A",
                "EngName": "EA",
                "Level": "1",
                "Grade": "2",
                "LocalDesc": "desc",
                "Type": "10",
                "Kind": "20",
                "Property": "30",
                "SetTID": "1",
            }
        )
        set_row = RawRecord(table="ItemSetTable", values={"TID": TraceValue("ItemSetTable", "TID", "1", "direct")})
        ability_row = RawRecord(
            table="ItemSetAbilityTable",
            values={"TID": TraceValue("ItemSetAbilityTable", "TID", "10", "direct")},
        )
        raw = ItemQueryResult(
            query="100",
            query_type="item_id",
            matched_items=[item],
            candidates=[],
            set_chain={"ItemSetTable": [set_row], "ItemSetAbilityTable": [ability_row]},
        )

        view = build_result_view_model(raw)
        self.assertIsInstance(view, ItemResultPageModel)
        self.assertEqual(view.basic_information.name, "basic_information")
        self.assertEqual(view.classification.name, "classification")
        self.assertEqual(view.source_information.name, "source_information")
        self.assertEqual(view.trust_status.name, "trust_status")
        self.assertEqual(view.equipment_chain.section.name, "equipment_chain")
        self.assertEqual(view.equipment_chain.state, "available")

    def test_multi_candidate_builds_candidate_oriented_model(self) -> None:
        c1 = _item_record({"TID": "1", "LocalName": "dup", "Type": "1", "Kind": "1", "Property": "1"})
        c2 = _item_record({"TID": "2", "LocalName": "dup", "Type": "1", "Kind": "1", "Property": "1"})
        raw = ItemQueryResult(
            query="dup",
            query_type="item_name",
            matched_items=[],
            candidates=[c1, c2],
            set_chain={"ItemSetTable": [], "ItemSetAbilityTable": []},
        )

        view = build_result_view_model(raw)
        self.assertIsInstance(view, CandidateResultModel)
        self.assertEqual(len(view.candidates), 2)
        self.assertTrue(all(candidate.equipment_chain.state != "available" for candidate in view.candidates))

    def test_direct_field_mapping_preserves_traceability(self) -> None:
        item = _item_record(
            {
                "TID": "100",
                "LocalName": "A",
                "EngName": "EA",
                "Level": "1",
                "Grade": "2",
                "LocalDesc": "desc",
                "Type": "10",
                "Kind": "20",
                "Property": "30",
            }
        )
        raw = ItemQueryResult("100", "item_id", [item], [], {"ItemSetTable": [], "ItemSetAbilityTable": []})

        view = build_result_view_model(raw)
        assert isinstance(view, ItemResultPageModel)
        tid_field = next(x for x in view.basic_information.fields if x.key == "TID")
        self.assertEqual(tid_field.value, "100")
        self.assertEqual(tid_field.source_table, "ItemTable")
        self.assertEqual(tid_field.source_field, "TID")
        self.assertEqual(tid_field.status, "direct")

    def test_derived_is_equipment_field(self) -> None:
        item = _item_record(
            {
                "TID": "100",
                "LocalName": "A",
                "Type": "10",
                "Kind": "20",
                "Property": "30",
                "SetTID": "0",
                "AP": "15",
            }
        )
        raw = ItemQueryResult("100", "item_id", [item], [], {"ItemSetTable": [], "ItemSetAbilityTable": []})

        view = build_result_view_model(raw)
        assert isinstance(view, ItemResultPageModel)
        is_equipment = next(x for x in view.classification.fields if x.key == "is_equipment")
        self.assertEqual(is_equipment.status, "derived")
        self.assertEqual(is_equipment.value, "可能是装备")

    def test_pending_confirmation_classification_output(self) -> None:
        item = _item_record({"TID": "100", "Type": "10", "Kind": "20", "Property": "30"})
        raw = ItemQueryResult("100", "item_id", [item], [], {"ItemSetTable": [], "ItemSetAbilityTable": []})

        view = build_result_view_model(raw)
        assert isinstance(view, ItemResultPageModel)
        category = next(x for x in view.classification.fields if x.key == "category_name_zh")
        self.assertEqual(category.status, "pending_confirmation")
        self.assertEqual(category.value, "待确认")


    def test_all_displayed_fields_keep_traceability_and_valid_status(self) -> None:
        item = _item_record(
            {
                "TID": "100",
                "LocalName": "A",
                "EngName": "EA",
                "Level": "1",
                "Grade": "2",
                "LocalDesc": "desc",
                "Type": "10",
                "Kind": "20",
                "Property": "30",
                "SetTID": "0",
            }
        )
        raw = ItemQueryResult("100", "item_id", [item], [], {"ItemSetTable": [], "ItemSetAbilityTable": []})

        view = build_result_view_model(raw)
        assert isinstance(view, ItemResultPageModel)
        allowed_status = {"direct", "derived", "pending_confirmation"}
        sections = [
            view.basic_information,
            view.classification,
            view.source_information,
            view.trust_status,
            view.equipment_chain.section,
        ]
        for section in sections:
            for field in section.fields:
                self.assertTrue(field.source_table)
                self.assertTrue(field.source_field)
                self.assertIn(field.status, allowed_status)

    def test_category_name_zh_remains_pending_confirmation_not_confirmed_label(self) -> None:
        item = _item_record({"TID": "100", "Type": "10", "Kind": "20", "Property": "30"})
        raw = ItemQueryResult("100", "item_id", [item], [], {"ItemSetTable": [], "ItemSetAbilityTable": []})

        view = build_result_view_model(raw)
        assert isinstance(view, ItemResultPageModel)
        category = next(x for x in view.classification.fields if x.key == "category_name_zh")
        self.assertEqual(category.value, "待确认")
        self.assertEqual(category.status, "pending_confirmation")

    def test_candidate_result_never_marks_equipment_chain_available(self) -> None:
        c1 = _item_record({"TID": "1", "LocalName": "dup", "Type": "1", "Kind": "1", "Property": "1", "AP": "10"})
        c2 = _item_record({"TID": "2", "LocalName": "dup", "Type": "1", "Kind": "1", "Property": "1", "SetTID": "3"})
        raw = ItemQueryResult(
            query="dup",
            query_type="item_name",
            matched_items=[],
            candidates=[c1, c2],
            set_chain={"ItemSetTable": [], "ItemSetAbilityTable": []},
        )

        view = build_result_view_model(raw)
        assert isinstance(view, CandidateResultModel)
        self.assertTrue(all(candidate.equipment_chain.state != "available" for candidate in view.candidates))
    def test_equipment_chain_not_applicable_for_non_equipment(self) -> None:
        item = _item_record({"TID": "100", "Type": "10", "Kind": "20", "Property": "30", "SetTID": "0", "AP": "0"})
        raw = ItemQueryResult("100", "item_id", [item], [], {"ItemSetTable": [], "ItemSetAbilityTable": []})

        view = build_result_view_model(raw)
        assert isinstance(view, ItemResultPageModel)
        self.assertEqual(view.equipment_chain.state, "not_applicable")


if __name__ == "__main__":
    unittest.main()
