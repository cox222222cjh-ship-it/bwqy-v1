from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RegressionSample:
    key: str
    query: str
    domain: str
    representative_reason: str
    whitelist_path_or_rule: str
    stable_behavior: str


ITEM_SAMPLES: tuple[RegressionSample, ...] = (
    RegressionSample(
        key="item_exact_tid_collision_guard",
        query="80",
        domain="item",
        representative_reason="纯数字 TID 同时存在 NPC/Item 碰撞，但 item 域显式查询仍应稳定命中 Item 80。",
        whitelist_path_or_rule="ItemTable.TID exact lookup；不因 NPC 同号 TID 改写 item 域结果。",
        stable_behavior="query_item('80') 返回唯一 Item 记录，且不引入跨域自动关联。",
    ),
    RegressionSample(
        key="item_exact_name",
        query="声望销售",
        domain="item",
        representative_reason="真实物品名，且还能作为 NPC shop 反向来源样本复用。",
        whitelist_path_or_rule="ItemTable.LocalName exact lookup。",
        stable_behavior="query_item('声望销售') 返回唯一 Item 20。",
    ),
    RegressionSample(
        key="item_set_chain",
        query="100010",
        domain="item",
        representative_reason="真实装备套装成员，能覆盖 ItemSetTable / ItemSetAbilityTable 链路。",
        whitelist_path_or_rule="ItemTable.SetTID -> ItemSetTable.TID -> ItemSetAbilityTable.TID。",
        stable_behavior="返回唯一 Item 100010，并保留至少 1 条 set 记录与至少 1 条 set ability 记录。",
    ),
    RegressionSample(
        key="item_duplicate_name",
        query="盾牌",
        domain="item",
        representative_reason="真实重名物品，可验证 item 域保守歧义行为。",
        whitelist_path_or_rule="ItemTable.LocalName duplicate candidates；不自动猜测唯一候选。",
        stable_behavior="query_item('盾牌') 保持 candidates>=2，且 matched_items 为空。",
    ),
)

NPC_SAMPLES: tuple[RegressionSample, ...] = (
    RegressionSample(
        key="npc_shop_owner",
        query="声望商店",
        domain="npc",
        representative_reason="真实 NPC 商店入口，能稳定验证 shop 白名单路径。",
        whitelist_path_or_rule="NpcTable.SaleTID -> SaleTable.SaleTID -> SaleTable.ItemTID -> ItemTable.TID。",
        stable_behavior="query_npc_or_item('声望商店') 返回 npc 域，shop section 至少包含 1 个直接商品关系。",
    ),
    RegressionSample(
        key="npc_drop_owner",
        query="哥布林池塘抢夺者",
        domain="npc",
        representative_reason="真实唯一名 NPC，含稳定掉落关系，可避免同名 NPC 噪音。",
        whitelist_path_or_rule="NpcTable.ItemDropTID -> ItemDropTable.TID -> ItemDropTable.DropItemNN -> ItemTable.TID。",
        stable_behavior="query_npc_or_item('哥布林池塘抢夺者') 返回 npc 域，drop section 至少包含 1 个直接掉落关系。",
    ),
    RegressionSample(
        key="npc_reverse_shop_item",
        query="声望销售",
        domain="npc",
        representative_reason="同一真实 item 样本可反向验证 shop 来源查询。",
        whitelist_path_or_rule="Item reverse lookup through SaleTable whitelist path。",
        stable_behavior="query_npc_or_item('声望销售') 返回 item 视角，并至少回指 1 个 NPC shop 来源。",
    ),
    RegressionSample(
        key="npc_numeric_ambiguity",
        query="80",
        domain="npc",
        representative_reason="真实 NPC/Item 同号 TID，可验证显式数值歧义约束。",
        whitelist_path_or_rule="纯数字同时命中 NPC TID 与 Item TID 时必须 ambiguous。",
        stable_behavior="query_npc_or_item('80') 返回 ambiguous，且不返回 sections。",
    ),
)

QUEST_SAMPLES: tuple[RegressionSample, ...] = (
    RegressionSample(
        key="quest_exact_name_and_drop",
        query="哥布林的异常繁殖",
        domain="quest",
        representative_reason="真实任务名，覆盖 quest exact lookup 与 quest-drop 解析。",
        whitelist_path_or_rule="QuestTable exact match + QuestDropTable.QuestTID 主事实来源。",
        stable_behavior="query_quest('哥布林的异常繁殖') 返回 Quest 1，并保留 confirmed quest_drops。",
    ),
    RegressionSample(
        key="quest_give_item",
        query="4",
        domain="quest",
        representative_reason="真实任务 TID，稳定覆盖 GiveItem1 路径。",
        whitelist_path_or_rule="QuestTable.GiveItem1 -> ItemTable.TID。",
        stable_behavior="query_quest('4') 返回 GiveItem1=20173（雷诺亚粉末）且状态 confirmed。",
    ),
    RegressionSample(
        key="quest_reward_and_vector_mission",
        query="5",
        domain="quest",
        representative_reason="真实任务同时包含向量 MissionTID、向量 RewardTID、confirmed reward item 与 quest drop。",
        whitelist_path_or_rule="QuestTable.MissionTID / RewardTID vector handling；Type=1 reward 才解析到 ItemTable。",
        stable_behavior="query_quest('5') 需保留两个 mission、至少一个 confirmed reward item，并保留 confirmed quest drop。",
    ),
    RegressionSample(
        key="quest_prev_link_vector_guard",
        query="926",
        domain="quest",
        representative_reason="真实 PrevQuest 向量字段，可验证保守单链接解释策略。",
        whitelist_path_or_rule="PrevQuest vector-typed conservative handling。",
        stable_behavior="query_quest('926') 返回 prev_quest.status=pending_confirmation，并输出 PrevQuest 向量说明 note。",
    ),
)

UNIFIED_SAMPLES: tuple[RegressionSample, ...] = (
    RegressionSample(
        key="unified_no_hint_item",
        query="声望销售",
        domain="unified",
        representative_reason="真实无 hint item 精确命中。",
        whitelist_path_or_rule="无 hint 时仅 item 域稳定命中，统一路由应落到 item。",
        stable_behavior="route_operator_query('声望销售') 返回 domain=item, status=exact_match。",
    ),
    RegressionSample(
        key="unified_no_hint_npc",
        query="声望商店",
        domain="unified",
        representative_reason="真实无 hint NPC 精确命中。",
        whitelist_path_or_rule="无 hint 时仅 npc 域稳定命中。",
        stable_behavior="route_operator_query('声望商店') 返回 domain=npc, status=exact_match。",
    ),
    RegressionSample(
        key="unified_no_hint_quest",
        query="哥布林的异常繁殖",
        domain="unified",
        representative_reason="真实无 hint Quest 精确命中。",
        whitelist_path_or_rule="无 hint 时仅 quest 域稳定命中。",
        stable_behavior="route_operator_query('哥布林的异常繁殖') 返回 domain=quest, status=exact_match。",
    ),
    RegressionSample(
        key="unified_cross_domain_ambiguity",
        query="哥布林的宝物",
        domain="unified",
        representative_reason="真实 item/quest 同名碰撞，可验证跨主域歧义。",
        whitelist_path_or_rule="跨 Item / Quest 主域同名命中时不自动选边。",
        stable_behavior="route_operator_query('哥布林的宝物') 返回 ambiguous，domain=None。",
    ),
    RegressionSample(
        key="unified_numeric_ambiguity",
        query="80",
        domain="unified",
        representative_reason="真实 NPC/Item 数字碰撞。",
        whitelist_path_or_rule="优先暴露 NPC 模块的 numeric ambiguity。",
        stable_behavior="route_operator_query('80') 返回 ambiguous，domain=None，并保留数值歧义 note。",
    ),
    RegressionSample(
        key="unified_not_found",
        query="MISSING_OPERATOR_SAMPLE",
        domain="unified",
        representative_reason="稳定的仓库外查询字符串，可验证 not_found envelope。",
        whitelist_path_or_rule="未命中任何白名单主域时返回 not_found。",
        stable_behavior="route_operator_query('MISSING_OPERATOR_SAMPLE') 返回 not_found，domain=None。",
    ),
    RegressionSample(
        key="unified_domain_hint",
        query="哥布林的宝物",
        domain="unified",
        representative_reason="同一歧义样本在显式 hint 下必须稳定落到指定域。",
        whitelist_path_or_rule="显式 domain_hint 优先于自动路由。",
        stable_behavior="item/quest domain_hint 都必须返回 exact_match 且分别落到 item / quest。",
    ),
)
