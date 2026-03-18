from __future__ import annotations

import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from item_query_v1.query_service import ItemQueryIndex
from item_query_v1.web_ui import init_app_state, query_to_page_state
from item_query_v1.result_view_model import CandidateResultModel, ItemResultPageModel


class WebUiTests(unittest.TestCase):
    def _build_index(self) -> ItemQueryIndex:
        row1 = {
            "TID": "100",
            "LocalName": "ONE",
            "EngName": "ONE_EN",
            "Type": "1",
            "Kind": "1",
            "Property": "1",
            "SetTID": "0",
            "AP": "0",
            "DP": "0",
            "BP": "0",
            "CP": "0",
        }
        row2 = {
            "TID": "200",
            "LocalName": "DUP",
            "EngName": "DUP_A",
            "Type": "1",
            "Kind": "1",
            "Property": "1",
            "SetTID": "0",
            "AP": "0",
            "DP": "0",
            "BP": "0",
            "CP": "0",
        }
        row3 = {
            "TID": "201",
            "LocalName": "DUP",
            "EngName": "DUP_B",
            "Type": "1",
            "Kind": "1",
            "Property": "1",
            "SetTID": "0",
            "AP": "0",
            "DP": "0",
            "BP": "0",
            "CP": "0",
        }
        return ItemQueryIndex(
            tables={},
            by_tid={"100": row1, "200": row2, "201": row3},
            by_local_name={"ONE": [row1], "DUP": [row2, row3]},
            by_eng_name={"ONE_EN": [row1], "DUP_A": [row2], "DUP_B": [row3]},
            item_set_by_tid={},
            set_ability_by_tid={},
        )

    def test_single_result_state(self) -> None:
        state = query_to_page_state(self._build_index(), "100")
        self.assertFalse(state.no_result)
        self.assertIsNone(state.error)
        self.assertIsInstance(state.result, ItemResultPageModel)

    def test_candidate_state(self) -> None:
        state = query_to_page_state(self._build_index(), "DUP")
        self.assertFalse(state.no_result)
        self.assertIsInstance(state.result, CandidateResultModel)
        assert isinstance(state.result, CandidateResultModel)
        self.assertEqual(len(state.result.candidates), 2)

    def test_no_result_state(self) -> None:
        state = query_to_page_state(self._build_index(), "NOT_FOUND")
        self.assertTrue(state.no_result)
        self.assertIsNone(state.result)

    def test_candidate_render_keeps_traceability_and_pending_visible(self) -> None:
        from item_query_v1.web_ui import build_html

        state = query_to_page_state(self._build_index(), "DUP")
        html = build_html(state)
        self.assertIn("来源追踪", html)
        self.assertIn("ItemTable.TID", html)
        self.assertIn("ItemTable.SetTID|AP|DP|BP|CP", html)
        self.assertIn("derived", html)
        self.assertIn("pending_confirmation", html)

    def test_detail_render_shows_status_source_and_pending_warning(self) -> None:
        from item_query_v1.web_ui import build_html

        state = query_to_page_state(self._build_index(), "100")
        html = build_html(state)
        self.assertIn("可信状态", html)
        self.assertIn("来源", html)
        self.assertIn("pending_confirmation", html)
        self.assertIn("包含 pending_confirmation 字段，请谨慎使用。", html)

    def test_detail_render_localizes_safe_labels_and_keeps_cautious_unknowns(
        self,
    ) -> None:
        from item_query_v1.web_ui import build_html

        state = query_to_page_state(self._build_index(), "100")
        html = build_html(state)
        self.assertIn("物品ID", html)
        self.assertIn("物品名称", html)
        self.assertIn("英文键", html)
        self.assertIn("物品描述", html)
        self.assertIn("Level（待确认含义）", html)
        self.assertIn("Grade（待确认含义）", html)
        self.assertIn("direct（直接读取）", html)
        self.assertIn("derived（推断）", html)
        self.assertIn("pending_confirmation（待确认）", html)

    def test_startup_error_state(self) -> None:
        app_state = init_app_state(
            index_builder=lambda: (_ for _ in ()).throw(RuntimeError("boom"))
        )
        self.assertIsNotNone(app_state.startup_error)
        self.assertIn("索引加载失败", app_state.startup_error or "")


if __name__ == "__main__":
    unittest.main()
