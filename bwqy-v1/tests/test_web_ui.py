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

    def test_startup_error_state(self) -> None:
        app_state = init_app_state(index_builder=lambda: (_ for _ in ()).throw(RuntimeError("boom")))
        self.assertIsNotNone(app_state.startup_error)
        self.assertIn("索引加载失败", app_state.startup_error or "")


if __name__ == "__main__":
    unittest.main()
