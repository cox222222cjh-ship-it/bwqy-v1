from __future__ import annotations

import unittest
from unittest.mock import patch
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from item_query_v1.quest_query import (
    QuestQueryIndex,
    build_quest_query_index,
    query_quest,
)


class QuestQueryV1Tests(unittest.TestCase):
    def _build_index(self) -> QuestQueryIndex:
        quest_main = {
            "TID": "100",
            "LocalTitle": "QUEST_MAIN",
            "PrevQuest": "90",
            "NextQuest": "110",
            "GiveItem1": "2000",
            "GiveItemCnt1": "2",
            "GiveItem2": "9999",
            "GiveItemCnt2": "1",
            "MissionTID": "3000",
            "RewardTID": "4000",
            "DropTID": "777",
        }
        quest_prev = {"TID": "90", "LocalTitle": "QUEST_PREV"}
        quest_next = {"TID": "110", "LocalTitle": "QUEST_NEXT"}
        quest_dup_a = {"TID": "120", "LocalTitle": "DUP_QUEST"}
        quest_dup_b = {"TID": "121", "LocalTitle": "DUP_QUEST"}
        mission = {"TID": "3000", "LocalTitle": "MISSION_TITLE", "LocalPurpose": "MISSION_PURPOSE"}
        reward_item = {"TID": "4000", "Type": "1", "Value": "2000", "Count": "1", "IsSelect": "0"}
        reward_pending = {"TID": "4000", "Type": "3", "Value": "5555", "Count": "9", "IsSelect": "0"}
        quest_drop = {
            "TID": "401",
            "QuestTID": "100",
            "NpcTID": "5000",
            "ItemTID": "2001",
            "DropRate": "9000",
            "DropStack": "1",
            "DropAll": "1",
        }
        item_give = {"TID": "2000", "LocalName": "ITEM_GIVE"}
        item_drop = {"TID": "2001", "LocalName": "ITEM_DROP"}
        npc_drop = {"TID": "5000", "LocalName": "NPC_DROP"}

        return QuestQueryIndex(
            quest_by_tid={
                "90": quest_prev,
                "100": quest_main,
                "110": quest_next,
                "120": quest_dup_a,
                "121": quest_dup_b,
            },
            quests_by_name={
                "QUEST_MAIN": [quest_main],
                "DUP_QUEST": [quest_dup_a, quest_dup_b],
            },
            mission_by_tid={"3000": mission},
            rewards_by_tid={"4000": [reward_item, reward_pending]},
            drops_by_quest_tid={"100": [quest_drop]},
            items_by_tid={"2000": item_give, "2001": item_drop},
            npcs_by_tid={"5000": npc_drop},
        )

    def test_single_quest_match_returns_only_whitelist_sections(self) -> None:
        result = query_quest(self._build_index(), "100")

        self.assertEqual(result.status, "ok")
        assert result.payload is not None
        self.assertEqual(result.quest.tid, 100)
        self.assertEqual(result.payload.prev_quest.status, "confirmed")
        self.assertEqual(result.payload.next_quest.status, "confirmed")
        self.assertEqual(len(result.payload.give_items), 2)
        self.assertEqual(len(result.payload.missions), 1)
        self.assertEqual(len(result.payload.rewards), 2)
        self.assertEqual(len(result.payload.quest_drops), 1)
        self.assertEqual([(x.tid, x.name) for x in result.payload.related_items], [(2000, "ITEM_GIVE"), (2001, "ITEM_DROP")])
        self.assertEqual([(x.tid, x.name) for x in result.payload.related_npcs], [(5000, "NPC_DROP")])
        self.assertFalse(hasattr(result.payload, "quest_scenes"))

    def test_name_search_multiple_hits_returns_ambiguous(self) -> None:
        result = query_quest(self._build_index(), "DUP_QUEST")

        self.assertEqual(result.status, "ambiguous")
        self.assertIsNone(result.payload)
        self.assertEqual([candidate.tid for candidate in result.candidates], [120, 121])

    def test_missing_prev_next_or_give_item_references_return_missing(self) -> None:
        index = self._build_index()
        index.quest_by_tid["100"] = {
            **index.quest_by_tid["100"],
            "PrevQuest": "0",
            "NextQuest": "999",
            "GiveItem2": "8888",
        }
        result = query_quest(index, "100")

        assert result.payload is not None
        self.assertEqual(result.payload.prev_quest.status, "missing")
        self.assertEqual(result.payload.next_quest.status, "missing")
        missing_give = next(item for item in result.payload.give_items if item.slot == "GiveItem2")
        self.assertEqual(missing_give.status, "missing")
        self.assertIsNone(missing_give.item_name)

    def test_vector_mission_field_resolves_multiple_ids_in_order(self) -> None:
        index = self._build_index()
        index.quest_by_tid["100"] = {
            **index.quest_by_tid["100"],
            "MissionTID": "3000|3001|0|9999",
        }
        index.mission_by_tid["3001"] = {
            "TID": "3001",
            "LocalTitle": "MISSION_TWO",
            "LocalPurpose": "MISSION_TWO_PURPOSE",
        }

        result = query_quest(index, "100")

        assert result.payload is not None
        self.assertEqual(
            [mission.mission_tid for mission in result.payload.missions],
            [3000, 3001, 9999],
        )
        self.assertEqual(
            [mission.status for mission in result.payload.missions],
            ["confirmed", "confirmed", "missing"],
        )

    def test_vector_reward_field_resolves_multiple_ids_in_order(self) -> None:
        index = self._build_index()
        index.quest_by_tid["100"] = {
            **index.quest_by_tid["100"],
            "RewardTID": "4000|4001|0|9998",
        }
        index.rewards_by_tid["4001"] = [
            {
                "TID": "4001",
                "Type": "1",
                "Value": "2001",
                "Count": "2",
                "IsSelect": "1",
            }
        ]

        result = query_quest(index, "100")

        assert result.payload is not None
        self.assertEqual(
            [reward.reward_tid for reward in result.payload.rewards],
            [4000, 4000, 4001, 9998],
        )
        self.assertEqual(result.payload.rewards[2].resolved_item_tid, 2001)
        self.assertEqual(result.payload.rewards[2].status, "confirmed")
        self.assertEqual(result.payload.rewards[3].status, "missing")

    def test_vector_prev_next_fields_are_handled_conservatively(self) -> None:
        index = self._build_index()
        index.quest_by_tid["100"] = {
            **index.quest_by_tid["100"],
            "PrevQuest": "90|91",
            "NextQuest": "110|111",
        }
        index.quest_by_tid["91"] = {"TID": "91", "LocalTitle": "QUEST_PREV_ALT"}
        index.quest_by_tid["111"] = {"TID": "111", "LocalTitle": "QUEST_NEXT_ALT"}

        result = query_quest(index, "100")

        assert result.payload is not None
        self.assertEqual(result.payload.prev_quest.tid, 90)
        self.assertEqual(result.payload.prev_quest.status, "pending_confirmation")
        self.assertEqual(result.payload.next_quest.tid, 110)
        self.assertEqual(result.payload.next_quest.status, "pending_confirmation")
        self.assertTrue(any("PrevQuest 是向量字段" in note for note in result.notes))
        self.assertTrue(any("NextQuest 是向量字段" in note for note in result.notes))

    def test_reward_value_is_not_auto_linked_only_because_it_is_numeric(self) -> None:
        result = query_quest(self._build_index(), "100")

        assert result.payload is not None
        pending_reward = next(reward for reward in result.payload.rewards if reward.type == "3")
        self.assertEqual(pending_reward.status, "pending_confirmation")
        self.assertIsNone(pending_reward.resolved_item_tid)
        self.assertEqual(pending_reward.value, 5555)

    def test_quest_drop_uses_quest_tid_as_primary_fact_source(self) -> None:
        result = query_quest(self._build_index(), "100")

        assert result.payload is not None
        self.assertEqual(len(result.payload.quest_drops), 1)
        self.assertEqual(result.payload.quest_drops[0].quest_tid, 100)
        self.assertTrue(any("QuestTable.DropTID" in note for note in result.notes))

    def test_vector_drop_tid_is_diagnostic_only_and_does_not_crash(self) -> None:
        index = self._build_index()
        index.quest_by_tid["100"] = {
            **index.quest_by_tid["100"],
            "DropTID": "777|778|0",
        }

        result = query_quest(index, "100")

        assert result.payload is not None
        self.assertEqual(len(result.payload.quest_drops), 1)
        self.assertEqual(result.payload.quest_drops[0].quest_tid, 100)
        self.assertTrue(any("DropTID 是向量字段" in note for note in result.notes))

    def test_build_index_uses_real_whitelist_field_names(self) -> None:
        tables = {
            "QuestTable": [
                {
                    "TID": "100",
                    "LocalTitle": "QUEST_MAIN",
                    "PrevQuest": "90|91",
                    "NextQuest": "110",
                    "GiveItem1": "2000",
                    "GiveItemCnt1": "1",
                    "GiveItem2": "0",
                    "GiveItemCnt2": "0",
                    "MissionTID": "3000|3001",
                    "RewardTID": "4000|4001",
                    "DropTID": "777|778",
                }
            ],
            "QuestMissionTable": [
                {"TID": "3000", "LocalTitle": "MISSION_A", "LocalPurpose": "A"},
                {"TID": "3001", "LocalTitle": "MISSION_B", "LocalPurpose": "B"},
            ],
            "QuestRewardTable": [
                {"TID": "4000", "Type": "1", "Value": "2000", "Count": "1", "IsSelect": "0"},
                {"TID": "4001", "Type": "3", "Value": "555", "Count": "8", "IsSelect": "0"},
            ],
            "QuestDropTable": [
                {
                    "TID": "7000",
                    "QuestTID": "100",
                    "NpcTID": "5000",
                    "ItemTID": "2001",
                    "DropRate": "9000",
                    "DropStack": "1",
                    "DropAll": "1",
                }
            ],
            "ItemTable": [
                {"TID": "2000", "LocalName": "ITEM_GIVE"},
                {"TID": "2001", "LocalName": "ITEM_DROP"},
            ],
            "NpcTable": [
                {"TID": "5000", "LocalName": "NPC_DROP"},
            ],
        }

        with patch("item_query_v1.quest_query.resolve_tables_dir", return_value=Path("/tmp/quest")), patch(
            "item_query_v1.quest_query.load_selected_tables",
            return_value=tables,
        ):
            index = build_quest_query_index()

        self.assertIn("100", index.quest_by_tid)
        self.assertIn("QUEST_MAIN", index.quests_by_name)
        result = query_quest(index, "100")
        assert result.payload is not None
        self.assertEqual([mission.mission_tid for mission in result.payload.missions], [3000, 3001])
        self.assertEqual(result.payload.prev_quest.status, "pending_confirmation")
        self.assertEqual(len(result.payload.rewards), 2)
        self.assertEqual(result.payload.quest_drops[0].npc_tid, 5000)

    def test_not_found_returns_stable_shape(self) -> None:
        result = query_quest(self._build_index(), "404")

        self.assertEqual(result.status, "not_found")
        self.assertIsNone(result.quest)
        self.assertEqual(result.candidates, [])
        self.assertIsNone(result.payload)


if __name__ == "__main__":
    unittest.main()
