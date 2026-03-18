# Design: build-operator-npc-drop-shop-query

## Overview

本次 change 不改写 `item-query-v1` 的闭包目标，而是在其旁边增加一个**最小运营查询路径**：

- NPC -> shop items
- NPC -> drop items
- Item -> NPC shop sources
- Item -> NPC drop sources

设计原则仍然是“结果可信优先于覆盖完整”。

## Data strategy

只读取以下四张表：

- `NpcTable`
- `SaleTable`
- `ItemDropTable`
- `ItemTable`

只建立以下索引：

- NPC: `TID` / `LocalName`
- Item: `TID` / `LocalName`
- `SaleTID -> SaleTable[]`
- `ItemDropTID -> ItemDropTable`

## Relation strategy

只允许两条高置信业务关系：

1. `NpcTable.SaleTID -> SaleTable.SaleTID -> SaleTable.ItemTID -> ItemTable.TID`
2. `NpcTable.ItemDropTID -> ItemDropTable.TID -> ItemDropTable.DropItemXX -> ItemTable.TID`

明确不做：

- 基于同名 `TID` 的泛化连边
- `MapDropTID` / `ItemDropWorldTable` 默认升级
- quest / world / map 扩展

## Result model

结果按 section 输出：

- owner record（NPC 或 Item）
- relation type（shop / drop）
- related records

每条 related record 必须包含：

- NPC record
- Item record
- source path
- trace records
- trust status

## Query behavior

- 若输入命中 NPC，则优先返回 NPC 视角结果。
- 若未命中 NPC 但命中 Item，则返回 Item 视角结果。
- 空值、`0`、坏引用统一视为空关系，不构造“待确认关系”冒充事实。

## Risks and mitigations

风险：

1. NPC TID 与 Item TID 数值可能碰撞。
2. `ItemDropTable` 中存在无效 item 引用。
3. 需求容易继续膨胀到 quest/world。

应对：

1. 查询时按业务域索引分开命中，不按同名字段泛化。
2. 只有能在 `ItemTable` 找到目标 item 时才输出关系。
3. 用 OpenSpec 明确把后续域列为 deferred。
