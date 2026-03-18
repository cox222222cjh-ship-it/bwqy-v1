from __future__ import annotations

import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from item_query_v1.npc_shop_drop_query import query_npc_or_item
from item_query_v1.query_service import ItemQueryIndex


class NpcShopDropQueryTests(unittest.TestCase):
    def _build_index(self) -> ItemQueryIndex:
        item_a = {"TID": "100", "LocalName": "ITEM_A"}
        item_b = {"TID": "101", "LocalName": "ITEM_B"}
        unrelated_item = {"TID": "500", "LocalName": "COLLISION_ONLY"}
        npc_shop = {"TID": "200", "LocalName": "NPC_SHOP", "SaleTID": "10", "ItemDropTID": "0"}
        npc_drop = {"TID": "201", "LocalName": "NPC_DROP", "SaleTID": "0", "ItemDropTID": "20"}
        npc_invalid = {"TID": "202", "LocalName": "NPC_INVALID", "SaleTID": "0", "ItemDropTID": "999"}
        npc_collision = {"TID": "500", "LocalName": "NPC_COLLISION", "SaleTID": "40", "ItemDropTID": "0"}

        sale_row = {"TID": "1", "SaleTID": "10", "ItemTID": "100"}
        unrelated_sale_row = {"TID": "2", "SaleTID": "40", "ItemTID": "9999"}
        drop_row = {
            "TID": "20",
            "DropItem01": "101",
            "DropItem02": "0",
        }

        return ItemQueryIndex(
            tables={},
            by_tid={"100": item_a, "101": item_b, "500": unrelated_item},
            by_local_name={
                "ITEM_A": [item_a],
                "ITEM_B": [item_b],
                "COLLISION_ONLY": [unrelated_item],
            },
            by_eng_name={},
            item_set_by_tid={},
            set_ability_by_tid={},
            npc_by_tid={
                "200": npc_shop,
                "201": npc_drop,
                "202": npc_invalid,
                "500": npc_collision,
            },
            npc_by_local_name={
                "NPC_SHOP": [npc_shop],
                "NPC_DROP": [npc_drop],
                "NPC_INVALID": [npc_invalid],
                "NPC_COLLISION": [npc_collision],
            },
            sale_items_by_sale_tid={"10": [sale_row], "40": [unrelated_sale_row]},
            drop_rows_by_tid={"20": drop_row},
        )

    def test_npc_with_valid_sale_tid_links_to_shop_items(self) -> None:
        result = query_npc_or_item(self._build_index(), "NPC_SHOP")
        shop_section = next(section for section in result.sections if section.relation_type == "shop")

        self.assertEqual(result.query_kind, "npc")
        self.assertEqual(len(shop_section.related_records), 1)
        relation = shop_section.related_records[0]
        self.assertEqual(relation.item_record.values["TID"].raw_value, "100")
        self.assertIn("NpcTable.SaleTID", relation.source_path)

    def test_npc_with_valid_item_drop_tid_links_to_drop_items(self) -> None:
        result = query_npc_or_item(self._build_index(), "NPC_DROP")
        drop_section = next(section for section in result.sections if section.relation_type == "drop")

        self.assertEqual(len(drop_section.related_records), 1)
        relation = drop_section.related_records[0]
        self.assertEqual(relation.item_record.values["TID"].raw_value, "101")
        self.assertIn("ItemDropTable.DropItem01", relation.source_path)

    def test_item_reverse_lookup_returns_matching_npc_sale_sources(self) -> None:
        result = query_npc_or_item(self._build_index(), "ITEM_A")
        shop_section = next(section for section in result.sections if section.relation_type == "shop")

        self.assertEqual(result.query_kind, "item")
        self.assertEqual(len(shop_section.related_records), 1)
        relation = shop_section.related_records[0]
        self.assertEqual(relation.npc_record.values["TID"].raw_value, "200")

    def test_item_reverse_lookup_returns_matching_npc_drop_sources(self) -> None:
        result = query_npc_or_item(self._build_index(), "101")
        drop_section = next(section for section in result.sections if section.relation_type == "drop")

        self.assertEqual(result.query_kind, "item")
        self.assertEqual(len(drop_section.related_records), 1)
        relation = drop_section.related_records[0]
        self.assertEqual(relation.npc_record.values["TID"].raw_value, "201")

    def test_missing_zero_or_invalid_relation_ids_are_handled_safely(self) -> None:
        invalid_result = query_npc_or_item(self._build_index(), "NPC_INVALID")
        invalid_drop = next(
            section for section in invalid_result.sections if section.relation_type == "drop"
        )
        invalid_shop = next(
            section for section in invalid_result.sections if section.relation_type == "shop"
        )

        self.assertEqual(invalid_drop.related_records, [])
        self.assertEqual(invalid_shop.related_records, [])

    def test_no_false_positive_relations_from_unrelated_tid_collisions(self) -> None:
        result = query_npc_or_item(self._build_index(), "500")

        self.assertEqual(result.query_kind, "npc")
        shop_section = next(section for section in result.sections if section.relation_type == "shop")
        drop_section = next(section for section in result.sections if section.relation_type == "drop")
        self.assertEqual(shop_section.related_records, [])
        self.assertEqual(drop_section.related_records, [])


if __name__ == "__main__":
    unittest.main()
