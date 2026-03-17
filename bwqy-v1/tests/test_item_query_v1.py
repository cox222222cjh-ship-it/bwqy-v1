from __future__ import annotations

import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from item_query_v1.csv_loader import load_csv_records, resolve_tables_dir
from item_query_v1.query_service import ItemQueryIndex, build_item_query_index, query_item


class ItemQueryV1Tests(unittest.TestCase):
    def test_item_table_skips_metadata_rows(self) -> None:
        tables_dir = resolve_tables_dir()
        rows = load_csv_records("ItemTable", tables_dir)
        self.assertGreater(len(rows), 0)
        self.assertEqual(rows[0]["TID"], "1")

    def test_query_by_item_id_exact(self) -> None:
        index = build_item_query_index()
        result = query_item(index, "1")
        self.assertEqual(result.query_type, "item_id")
        self.assertEqual(len(result.matched_items), 1)
        self.assertEqual(result.matched_items[0].values["TID"].raw_value, "1")

    def test_query_by_item_name_returns_stable_result(self) -> None:
        index = build_item_query_index()
        # 使用英文键，避免本地环境编码差异导致中文样例不稳定。
        result = query_item(index, "ITM_Name_000001")
        self.assertEqual(result.query_type, "item_name")
        self.assertEqual(len(result.matched_items), 1)
        self.assertEqual(result.matched_items[0].values["TID"].raw_value, "1")

    def test_multi_candidate_name_query_returns_candidates_without_global_set_chain(self) -> None:
        row1 = {"TID": "9001", "LocalName": "DUP_NAME", "EngName": "E1", "SetTID": "1"}
        row2 = {"TID": "9002", "LocalName": "DUP_NAME", "EngName": "E2", "SetTID": "2"}
        set_row1 = {"TID": "1", "SetAbilityTID": "10"}
        set_row2 = {"TID": "2", "SetAbilityTID": "20"}
        ability_row1 = {"TID": "10", "ReqTotal": "2", "LocalDesc": "A"}
        ability_row2 = {"TID": "20", "ReqTotal": "3", "LocalDesc": "B"}

        index = ItemQueryIndex(
            tables={},
            by_tid={"9001": row1, "9002": row2},
            by_local_name={"DUP_NAME": [row1, row2]},
            by_eng_name={"E1": [row1], "E2": [row2]},
            item_set_by_tid={"1": set_row1, "2": set_row2},
            set_ability_by_tid={"10": ability_row1, "20": ability_row2},
        )

        result = query_item(index, "DUP_NAME")
        self.assertEqual(len(result.matched_items), 0)
        self.assertEqual(len(result.candidates), 2)
        self.assertEqual(result.set_chain["ItemSetTable"], [])
        self.assertEqual(result.set_chain["ItemSetAbilityTable"], [])

    def test_single_match_can_attach_set_chain(self) -> None:
        index = build_item_query_index()
        result = query_item(index, "ITM_Name_000826")
        self.assertEqual(len(result.matched_items), 1)
        self.assertGreater(len(result.set_chain["ItemSetTable"]), 0)
        self.assertGreater(len(result.set_chain["ItemSetAbilityTable"]), 0)


if __name__ == "__main__":
    unittest.main()
