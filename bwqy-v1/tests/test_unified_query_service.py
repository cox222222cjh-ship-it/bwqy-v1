from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from item_query_v1.query_service import ItemQueryIndex, ItemQueryResult
from item_query_v1.quest_query import QuestQueryIndex, QuestQueryResult
from item_query_v1.unified_query_service import (
    UnifiedQueryRouterIndex,
    route_operator_query,
)


class UnifiedQueryServiceTests(unittest.TestCase):
    def _build_router_index(self) -> UnifiedQueryRouterIndex:
        item_exact = {"TID": "100", "LocalName": "ITEM_EXACT", "EngName": "ITEM_EXACT", "SetTID": "0"}
        item_npc_reverse = {"TID": "101", "LocalName": "ITEM_DROP", "EngName": "ITEM_DROP", "SetTID": "0"}
        item_numeric_collision = {"TID": "500", "LocalName": "ITEM_COLLISION", "EngName": "ITEM_COLLISION", "SetTID": "0"}
        item_quest_collision = {"TID": "900", "LocalName": "QUEST_SHARED", "EngName": "QUEST_SHARED", "SetTID": "0"}
        item_dup_a = {"TID": "700", "LocalName": "ITEM_DUP", "EngName": "ITEM_DUP_A", "SetTID": "0"}
        item_dup_b = {"TID": "701", "LocalName": "ITEM_DUP", "EngName": "ITEM_DUP_B", "SetTID": "0"}

        npc_exact = {"TID": "200", "LocalName": "NPC_EXACT", "SaleTID": "10", "ItemDropTID": "0"}
        npc_drop = {"TID": "201", "LocalName": "NPC_DROP", "SaleTID": "0", "ItemDropTID": "20"}
        npc_collision = {"TID": "500", "LocalName": "NPC_COLLISION", "SaleTID": "0", "ItemDropTID": "0"}

        sale_row = {"TID": "1", "SaleTID": "10", "ItemTID": "100"}
        drop_row = {"TID": "20", "DropItem01": "101", "DropItem02": "0"}

        item_index = ItemQueryIndex(
            tables={},
            by_tid={
                "100": item_exact,
                "101": item_npc_reverse,
                "500": item_numeric_collision,
                "700": item_dup_a,
                "701": item_dup_b,
                "900": item_quest_collision,
            },
            by_local_name={
                "ITEM_EXACT": [item_exact],
                "ITEM_DROP": [item_npc_reverse],
                "ITEM_COLLISION": [item_numeric_collision],
                "ITEM_DUP": [item_dup_a, item_dup_b],
                "QUEST_SHARED": [item_quest_collision],
            },
            by_eng_name={
                "ITEM_EXACT": [item_exact],
                "ITEM_DROP": [item_npc_reverse],
                "ITEM_COLLISION": [item_numeric_collision],
                "ITEM_DUP_A": [item_dup_a],
                "ITEM_DUP_B": [item_dup_b],
                "QUEST_SHARED": [item_quest_collision],
            },
            item_set_by_tid={},
            set_ability_by_tid={},
        )

        npc_index = ItemQueryIndex(
            tables={},
            by_tid={
                "100": item_exact,
                "101": item_npc_reverse,
                "500": item_numeric_collision,
                "900": item_quest_collision,
            },
            by_local_name={
                "ITEM_EXACT": [item_exact],
                "ITEM_DROP": [item_npc_reverse],
                "ITEM_COLLISION": [item_numeric_collision],
                "QUEST_SHARED": [item_quest_collision],
            },
            by_eng_name={},
            item_set_by_tid={},
            set_ability_by_tid={},
            npc_by_tid={"200": npc_exact, "201": npc_drop, "500": npc_collision},
            npc_by_local_name={
                "NPC_EXACT": [npc_exact],
                "NPC_DROP": [npc_drop],
                "NPC_COLLISION": [npc_collision],
            },
            sale_items_by_sale_tid={"10": [sale_row]},
            drop_rows_by_tid={"20": drop_row},
        )

        quest_main = {
            "TID": "300",
            "LocalTitle": "QUEST_EXACT",
            "PrevQuest": "0",
            "NextQuest": "0",
            "GiveItem1": "100",
            "GiveItemCnt1": "1",
            "GiveItem2": "0",
            "GiveItemCnt2": "0",
            "MissionTID": "0",
            "RewardTID": "0",
            "DropTID": "0",
        }
        quest_shared = {
            "TID": "301",
            "LocalTitle": "QUEST_SHARED",
            "PrevQuest": "0",
            "NextQuest": "0",
            "GiveItem1": "0",
            "GiveItemCnt1": "0",
            "GiveItem2": "0",
            "GiveItemCnt2": "0",
            "MissionTID": "0",
            "RewardTID": "0",
            "DropTID": "0",
        }
        quest_dup_a = {
            "TID": "302",
            "LocalTitle": "QUEST_DUP",
            "PrevQuest": "0",
            "NextQuest": "0",
            "GiveItem1": "0",
            "GiveItemCnt1": "0",
            "GiveItem2": "0",
            "GiveItemCnt2": "0",
            "MissionTID": "0",
            "RewardTID": "0",
            "DropTID": "0",
        }
        quest_dup_b = {
            "TID": "303",
            "LocalTitle": "QUEST_DUP",
            "PrevQuest": "0",
            "NextQuest": "0",
            "GiveItem1": "0",
            "GiveItemCnt1": "0",
            "GiveItem2": "0",
            "GiveItemCnt2": "0",
            "MissionTID": "0",
            "RewardTID": "0",
            "DropTID": "0",
        }

        quest_index = QuestQueryIndex(
            quest_by_tid={
                "300": quest_main,
                "301": quest_shared,
                "302": quest_dup_a,
                "303": quest_dup_b,
            },
            quests_by_name={
                "QUEST_EXACT": [quest_main],
                "QUEST_SHARED": [quest_shared],
                "QUEST_DUP": [quest_dup_a, quest_dup_b],
            },
            mission_by_tid={},
            rewards_by_tid={},
            drops_by_quest_tid={},
            items_by_tid={"100": item_exact},
            npcs_by_tid={},
        )

        return UnifiedQueryRouterIndex(
            item_index=item_index,
            npc_index=npc_index,
            quest_index=quest_index,
        )

    def test_item_exact_lookup_returns_normalized_item_envelope(self) -> None:
        result = route_operator_query(self._build_router_index(), "ITEM_EXACT", domain_hint="item")

        self.assertEqual(result.domain, "item")
        self.assertEqual(result.status, "exact_match")
        assert result.primary_payload is not None
        self.assertEqual(result.primary_payload.record.values["TID"].raw_value, "100")

    def test_no_hint_normal_item_lookup_prefers_canonical_item_domain(self) -> None:
        result = route_operator_query(self._build_router_index(), "ITEM_EXACT")

        self.assertEqual(result.domain, "item")
        self.assertEqual(result.status, "exact_match")
        assert result.primary_payload is not None
        self.assertIsInstance(result.primary_payload.result, ItemQueryResult)
        self.assertEqual(result.primary_payload.record.values["TID"].raw_value, "100")

    def test_npc_exact_lookup_returns_normalized_npc_envelope(self) -> None:
        result = route_operator_query(self._build_router_index(), "NPC_EXACT", domain_hint="npc")

        self.assertEqual(result.domain, "npc")
        self.assertEqual(result.status, "exact_match")
        assert result.primary_payload is not None
        self.assertEqual(result.primary_payload.record.values["TID"].raw_value, "200")

    def test_quest_exact_lookup_returns_normalized_quest_envelope(self) -> None:
        result = route_operator_query(self._build_router_index(), "QUEST_EXACT", domain_hint="quest")

        self.assertEqual(result.domain, "quest")
        self.assertEqual(result.status, "exact_match")
        assert result.primary_payload is not None
        self.assertEqual(result.primary_payload.record.tid, 300)

    def test_ambiguous_numeric_input_surfaces_explicit_disambiguation(self) -> None:
        result = route_operator_query(self._build_router_index(), "500")

        self.assertIsNone(result.domain)
        self.assertEqual(result.status, "ambiguous")
        self.assertTrue(any("同时命中 NPC TID 与 Item TID" in note for note in result.notes))

    def test_no_hint_item_domain_ambiguity_preserves_payload_and_candidates(self) -> None:
        result = route_operator_query(self._build_router_index(), "ITEM_DUP")

        self.assertEqual(result.domain, "item")
        self.assertEqual(result.status, "ambiguous")
        self.assertIsNotNone(result.primary_payload)
        assert result.primary_payload is not None
        self.assertIsInstance(result.primary_payload.result, ItemQueryResult)
        self.assertEqual(len(result.primary_payload.result.candidates), 2)

    def test_no_hint_quest_domain_ambiguity_preserves_payload_and_candidates(self) -> None:
        result = route_operator_query(self._build_router_index(), "QUEST_DUP")

        self.assertEqual(result.domain, "quest")
        self.assertEqual(result.status, "ambiguous")
        self.assertIsNotNone(result.primary_payload)
        assert result.primary_payload is not None
        self.assertIsInstance(result.primary_payload.result, QuestQueryResult)
        self.assertEqual(len(result.primary_payload.result.candidates), 2)

    def test_invalid_domain_hint_is_handled_explicitly(self) -> None:
        result = route_operator_query(self._build_router_index(), "ITEM_EXACT", domain_hint="world")

        self.assertIsNone(result.domain)
        self.assertEqual(result.status, "ambiguous")
        self.assertIsNone(result.primary_payload)
        self.assertTrue(any("无效的 domain_hint" in note for note in result.notes))

    def test_not_found_returns_stable_envelope(self) -> None:
        result = route_operator_query(self._build_router_index(), "MISSING_ENTRY")

        self.assertIsNone(result.domain)
        self.assertEqual(result.status, "not_found")
        self.assertIsNone(result.primary_payload)
        self.assertTrue(any("未在 Item / NPC / Quest 白名单域中找到匹配结果。" in note for note in result.notes))

    def test_routing_prefers_single_exact_domain_when_only_one_matches(self) -> None:
        npc_result = route_operator_query(self._build_router_index(), "NPC_DROP")
        quest_result = route_operator_query(self._build_router_index(), "QUEST_EXACT")

        self.assertEqual(npc_result.domain, "npc")
        self.assertEqual(npc_result.status, "exact_match")
        self.assertEqual(quest_result.domain, "quest")
        self.assertEqual(quest_result.status, "exact_match")

    def test_cross_domain_name_collision_requires_explicit_domain_selection(self) -> None:
        result = route_operator_query(self._build_router_index(), "QUEST_SHARED")

        self.assertIsNone(result.domain)
        self.assertEqual(result.status, "ambiguous")
        self.assertTrue(any("domain_hint=item|npc|quest" in note for note in result.notes))

    def test_item_domain_ambiguity_is_preserved_when_domain_hint_is_explicit(self) -> None:
        result = route_operator_query(self._build_router_index(), "ITEM_DUP", domain_hint="item")

        self.assertEqual(result.domain, "item")
        self.assertEqual(result.status, "ambiguous")
        self.assertIsNotNone(result.primary_payload)


if __name__ == "__main__":
    unittest.main()
