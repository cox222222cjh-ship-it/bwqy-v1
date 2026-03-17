from __future__ import annotations

import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from item_query_v1.csv_loader import load_csv_records, resolve_tables_dir
from item_query_v1.query_service import build_item_query_index, query_item


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


if __name__ == "__main__":
    unittest.main()
