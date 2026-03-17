from __future__ import annotations

import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from item_query_v1.query_service import ItemQueryIndex
from item_query_v1.result_view_model import CandidateResultModel, ItemResultPageModel
from item_query_v1.web_ui import build_html, query_to_page_state


class ItemQueryV1AcceptanceTests(unittest.TestCase):
    """Task 6: v1 查询到渲染的最小验收用例。"""

    @staticmethod
    def _build_index() -> ItemQueryIndex:
        equipment_item = {
            "TID": "500",
            "LocalName": "EQUIP_SWORD",
            "EngName": "EQUIP_SWORD_EN",
            "Type": "1",
            "Kind": "1",
            "Property": "1",
            "SetTID": "10",
            "AP": "15",
            "DP": "0",
            "BP": "0",
            "CP": "0",
        }
        non_equipment_item = {
            "TID": "600",
            "LocalName": "CONSUME_POTION",
            "EngName": "CONSUME_POTION_EN",
            "Type": "2",
            "Kind": "2",
            "Property": "2",
            "SetTID": "0",
            "AP": "0",
            "DP": "0",
            "BP": "0",
            "CP": "0",
        }
        duplicate_name_a = {
            "TID": "700",
            "LocalName": "DUP_NAME",
            "EngName": "DUP_NAME_A",
            "Type": "2",
            "Kind": "2",
            "Property": "2",
            "SetTID": "0",
            "AP": "0",
            "DP": "0",
            "BP": "0",
            "CP": "0",
        }
        duplicate_name_b = {
            "TID": "701",
            "LocalName": "DUP_NAME",
            "EngName": "DUP_NAME_B",
            "Type": "2",
            "Kind": "2",
            "Property": "2",
            "SetTID": "0",
            "AP": "0",
            "DP": "0",
            "BP": "0",
            "CP": "0",
        }
        item_set = {"TID": "10", "ItemTID": "500", "SetAbilityTID": "100|101"}
        set_ability_100 = {"TID": "100", "ReqTotal": "2", "LocalDesc": "2件效果"}
        set_ability_101 = {"TID": "101", "ReqTotal": "4", "LocalDesc": "4件效果"}

        return ItemQueryIndex(
            tables={},
            by_tid={
                "500": equipment_item,
                "600": non_equipment_item,
                "700": duplicate_name_a,
                "701": duplicate_name_b,
            },
            by_local_name={
                "EQUIP_SWORD": [equipment_item],
                "CONSUME_POTION": [non_equipment_item],
                "DUP_NAME": [duplicate_name_a, duplicate_name_b],
            },
            by_eng_name={
                "EQUIP_SWORD_EN": [equipment_item],
                "CONSUME_POTION_EN": [non_equipment_item],
                "DUP_NAME_A": [duplicate_name_a],
                "DUP_NAME_B": [duplicate_name_b],
            },
            item_set_by_tid={"10": item_set},
            set_ability_by_tid={"100": set_ability_100, "101": set_ability_101},
        )

    def test_acceptance_search_by_item_id_renders_v1_sections(self) -> None:
        state = query_to_page_state(self._build_index(), "500")
        self.assertFalse(state.no_result)
        self.assertIsInstance(state.result, ItemResultPageModel)

        html = build_html(state)
        self.assertIn("基础信息", html)
        self.assertIn("分类", html)
        self.assertIn("来源信息", html)
        self.assertIn("可信状态", html)
        self.assertIn("装备链路（state=available）", html)

    def test_acceptance_search_by_item_name_can_return_candidates(self) -> None:
        state = query_to_page_state(self._build_index(), "DUP_NAME")
        self.assertFalse(state.no_result)
        self.assertIsInstance(state.result, CandidateResultModel)

        html = build_html(state)
        self.assertIn("候选结果", html)
        self.assertIn("700", html)
        self.assertIn("701", html)

    def test_acceptance_equipment_result_has_non_ambiguous_chain(self) -> None:
        state = query_to_page_state(self._build_index(), "500")
        assert isinstance(state.result, ItemResultPageModel)

        self.assertEqual(state.result.equipment_chain.state, "available")
        self.assertEqual(len(state.result.equipment_chain.set_records), 1)
        self.assertEqual(len(state.result.equipment_chain.set_ability_records), 2)

    def test_acceptance_non_equipment_result_marks_chain_not_applicable(self) -> None:
        state = query_to_page_state(self._build_index(), "600")
        assert isinstance(state.result, ItemResultPageModel)

        self.assertEqual(state.result.equipment_chain.state, "not_applicable")
        html = build_html(state)
        self.assertIn("装备链路（state=not_applicable）", html)
        self.assertIn("不适用", html)

    def test_acceptance_pending_confirmation_is_visible_in_rendered_output(self) -> None:
        state = query_to_page_state(self._build_index(), "500")
        html = build_html(state)

        self.assertIn("pending_confirmation", html)
        self.assertIn("包含 pending_confirmation 字段，请谨慎使用。", html)
        self.assertIn("待确认", html)

    def test_acceptance_no_result_behavior(self) -> None:
        state = query_to_page_state(self._build_index(), "NOT_FOUND")
        self.assertTrue(state.no_result)
        self.assertIsNone(state.result)

        html = build_html(state)
        self.assertIn("无结果", html)
        self.assertIn("未命中任何物品", html)


if __name__ == "__main__":
    unittest.main()
