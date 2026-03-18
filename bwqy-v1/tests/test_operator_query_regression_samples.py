from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from item_query_v1.npc_shop_drop_query import build_npc_shop_drop_index, query_npc_or_item
from item_query_v1.query_service import build_item_query_index, query_item
from item_query_v1.quest_query import build_quest_query_index, query_quest
from item_query_v1.unified_query_service import build_unified_query_router_index, route_operator_query
from tests.operator_query_regression_samples import ITEM_SAMPLES, NPC_SAMPLES, QUEST_SAMPLES, UNIFIED_SAMPLES


class OperatorQueryRegressionSampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.item_index = build_item_query_index()
        cls.npc_index = build_npc_shop_drop_index()
        cls.quest_index = build_quest_query_index()
        cls.router_index = build_unified_query_router_index()

    def test_item_samples_remain_stable(self) -> None:
        sample_map = {sample.key: sample for sample in ITEM_SAMPLES}

        exact_tid = query_item(self.item_index, sample_map['item_exact_tid_collision_guard'].query)
        self.assertEqual([record.values['TID'].raw_value for record in exact_tid.matched_items], ['80'])
        self.assertEqual(exact_tid.candidates, [])

        exact_name = query_item(self.item_index, sample_map['item_exact_name'].query)
        self.assertEqual([record.values['TID'].raw_value for record in exact_name.matched_items], ['20'])

        set_chain = query_item(self.item_index, sample_map['item_set_chain'].query)
        self.assertEqual([record.values['TID'].raw_value for record in set_chain.matched_items], ['100010'])
        self.assertGreaterEqual(len(set_chain.set_chain['ItemSetTable']), 1)
        self.assertGreaterEqual(len(set_chain.set_chain['ItemSetAbilityTable']), 1)

        duplicate_name = query_item(self.item_index, sample_map['item_duplicate_name'].query)
        self.assertEqual(duplicate_name.matched_items, [])
        self.assertGreaterEqual(len(duplicate_name.candidates), 2)
        self.assertEqual(sorted(record.values['TID'].raw_value for record in duplicate_name.candidates[:2]), ['100', '190'])

    def test_npc_samples_remain_stable(self) -> None:
        sample_map = {sample.key: sample for sample in NPC_SAMPLES}

        shop_owner = query_npc_or_item(self.npc_index, sample_map['npc_shop_owner'].query)
        self.assertEqual(shop_owner.query_kind, 'npc')
        shop_section = next(section for section in shop_owner.sections if section.relation_type == 'shop')
        self.assertGreaterEqual(len(shop_section.related_records), 1)
        self.assertEqual(shop_section.owner_record.values['TID'].raw_value, '79')
        self.assertEqual(shop_section.related_records[0].item_record.values['TID'].raw_value, '20')
        self.assertIn('NpcTable.SaleTID', shop_section.related_records[0].source_path)

        drop_owner = query_npc_or_item(self.npc_index, sample_map['npc_drop_owner'].query)
        self.assertEqual(drop_owner.query_kind, 'npc')
        drop_section = next(section for section in drop_owner.sections if section.relation_type == 'drop')
        self.assertGreaterEqual(len(drop_section.related_records), 1)
        self.assertEqual(drop_section.owner_record.values['TID'].raw_value, '502')
        self.assertEqual(drop_section.related_records[0].item_record.values['TID'].raw_value, '2130001')
        self.assertIn('ItemDropTable.DropItem01', drop_section.related_records[0].source_path)

        reverse_shop_item = query_npc_or_item(self.npc_index, sample_map['npc_reverse_shop_item'].query)
        self.assertEqual(reverse_shop_item.query_kind, 'item')
        reverse_shop_section = next(section for section in reverse_shop_item.sections if section.relation_type == 'shop')
        self.assertGreaterEqual(len(reverse_shop_section.related_records), 1)
        self.assertEqual(reverse_shop_section.owner_record.values['TID'].raw_value, '20')
        self.assertEqual(reverse_shop_section.related_records[0].npc_record.values['TID'].raw_value, '79')

        numeric_ambiguity = query_npc_or_item(self.npc_index, sample_map['npc_numeric_ambiguity'].query)
        self.assertEqual(numeric_ambiguity.query_kind, 'ambiguous')
        self.assertEqual(numeric_ambiguity.sections, [])
        self.assertIn('同时命中 NPC TID 与 Item TID', numeric_ambiguity.note or '')

    def test_quest_samples_remain_stable(self) -> None:
        sample_map = {sample.key: sample for sample in QUEST_SAMPLES}

        exact_name_and_drop = query_quest(self.quest_index, sample_map['quest_exact_name_and_drop'].query)
        self.assertEqual(exact_name_and_drop.status, 'ok')
        assert exact_name_and_drop.payload is not None
        self.assertEqual(exact_name_and_drop.quest.tid, 1)
        self.assertGreaterEqual(len(exact_name_and_drop.payload.quest_drops), 1)
        self.assertTrue(all(drop.status == 'confirmed' for drop in exact_name_and_drop.payload.quest_drops))
        self.assertEqual(exact_name_and_drop.payload.quest_drops[0].npc_tid, 501)
        self.assertEqual(exact_name_and_drop.payload.quest_drops[0].item_tid, 20155)

        give_item = query_quest(self.quest_index, sample_map['quest_give_item'].query)
        self.assertEqual(give_item.status, 'ok')
        assert give_item.payload is not None
        self.assertEqual(give_item.quest.tid, 4)
        self.assertEqual([(item.item_tid, item.item_name, item.status) for item in give_item.payload.give_items], [(20173, '雷诺亚粉末', 'confirmed')])

        reward_and_vector = query_quest(self.quest_index, sample_map['quest_reward_and_vector_mission'].query)
        self.assertEqual(reward_and_vector.status, 'ok')
        assert reward_and_vector.payload is not None
        self.assertEqual(reward_and_vector.quest.tid, 5)
        self.assertEqual([mission.mission_tid for mission in reward_and_vector.payload.missions], [7, 8])
        confirmed_reward_items = [reward for reward in reward_and_vector.payload.rewards if reward.status == 'confirmed']
        self.assertGreaterEqual(len(confirmed_reward_items), 1)
        self.assertTrue(all(reward.resolved_item_tid is not None for reward in confirmed_reward_items))
        self.assertGreaterEqual(len(reward_and_vector.payload.quest_drops), 1)
        self.assertEqual(reward_and_vector.payload.quest_drops[0].npc_tid, 514)
        self.assertEqual(reward_and_vector.payload.quest_drops[0].item_tid, 20174)

        vector_prev = query_quest(self.quest_index, sample_map['quest_prev_link_vector_guard'].query)
        self.assertEqual(vector_prev.status, 'ok')
        assert vector_prev.payload is not None
        self.assertEqual(vector_prev.quest.tid, 926)
        self.assertEqual(vector_prev.payload.prev_quest.tid, 15103)
        self.assertEqual(vector_prev.payload.prev_quest.status, 'pending_confirmation')
        self.assertTrue(any('PrevQuest 是向量字段' in note for note in vector_prev.notes))

    def test_unified_samples_remain_stable(self) -> None:
        sample_map = {sample.key: sample for sample in UNIFIED_SAMPLES}

        no_hint_item = route_operator_query(self.router_index, sample_map['unified_no_hint_item'].query)
        self.assertEqual((no_hint_item.domain, no_hint_item.status), ('item', 'exact_match'))
        assert no_hint_item.primary_payload is not None
        self.assertEqual(no_hint_item.primary_payload.record.values['TID'].raw_value, '20')

        no_hint_npc = route_operator_query(self.router_index, sample_map['unified_no_hint_npc'].query)
        self.assertEqual((no_hint_npc.domain, no_hint_npc.status), ('npc', 'exact_match'))
        assert no_hint_npc.primary_payload is not None
        self.assertEqual(no_hint_npc.primary_payload.record.values['TID'].raw_value, '79')

        no_hint_quest = route_operator_query(self.router_index, sample_map['unified_no_hint_quest'].query)
        self.assertEqual((no_hint_quest.domain, no_hint_quest.status), ('quest', 'exact_match'))
        assert no_hint_quest.primary_payload is not None
        self.assertEqual(no_hint_quest.primary_payload.record.tid, 1)

        cross_domain = route_operator_query(self.router_index, sample_map['unified_cross_domain_ambiguity'].query)
        self.assertEqual((cross_domain.domain, cross_domain.status), (None, 'ambiguous'))
        self.assertTrue(any('domain_hint=item|npc|quest' in note for note in cross_domain.notes))

        numeric_ambiguity = route_operator_query(self.router_index, sample_map['unified_numeric_ambiguity'].query)
        self.assertEqual((numeric_ambiguity.domain, numeric_ambiguity.status), (None, 'ambiguous'))
        self.assertTrue(any('同时命中 NPC TID 与 Item TID' in note for note in numeric_ambiguity.notes))

        not_found = route_operator_query(self.router_index, sample_map['unified_not_found'].query)
        self.assertEqual((not_found.domain, not_found.status), (None, 'not_found'))
        self.assertTrue(any('未在 Item / NPC / Quest 白名单域中找到匹配结果。' in note for note in not_found.notes))

        hinted_item = route_operator_query(self.router_index, sample_map['unified_domain_hint'].query, domain_hint='item')
        hinted_quest = route_operator_query(self.router_index, sample_map['unified_domain_hint'].query, domain_hint='quest')
        self.assertEqual((hinted_item.domain, hinted_item.status), ('item', 'exact_match'))
        self.assertEqual((hinted_quest.domain, hinted_quest.status), ('quest', 'exact_match'))
        assert hinted_item.primary_payload is not None
        assert hinted_quest.primary_payload is not None
        self.assertEqual(hinted_item.primary_payload.record.values['TID'].raw_value, '20025')
        self.assertEqual(hinted_quest.primary_payload.record.tid, 7)


if __name__ == '__main__':
    unittest.main()
