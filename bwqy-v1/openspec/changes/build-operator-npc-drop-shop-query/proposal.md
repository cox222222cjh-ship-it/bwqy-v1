# Change Proposal: build-operator-npc-drop-shop-query

## Summary

在 `item-query-v1` 已收口的前提下，新增一个**最小运营向 NPC 掉落/商店查询能力**。本次 change 只覆盖 `NpcTable`、`ItemDropTable`、`SaleTable`、`ItemTable`，用于回答“哪个 NPC 掉这个物品 / 卖这个物品”“这个 NPC 掉什么 / 卖什么”。

## Why

运营主入口已经确认是 Item、NPC、Quest。继域白名单之后，最直接可交付的下一步就是 NPC 与 item 的 drop/shop 关系查询，因为这类问题高频、路径清晰、可通过高置信业务链路实现。

## Goals

1. 支持以 Item 名称或 TID 反查 NPC drop/shop 来源。
2. 支持以 NPC 名称或 TID 查询其 drop/shop 物品。
3. 结果必须保留来源链路与基础身份信息。
4. 只允许使用已确认的两条高置信业务关系链。
5. 缺少关系、关系无效、证据不足时不得伪造输出。

## Non-Goals

- Quest 查询
- Map/world 掉落导航
- Item 全关系扩展图
- 基于同名字段的自动连边
- broad full-table search
