# Spec: build-npc-drop-and-shop-query-v1

## ADDED Requirements

### Requirement: NPC shop relation query

系统 SHALL 支持基于以下高置信业务链路查询 NPC 商店关系：

- `NpcTable.SaleTID -> SaleTable.SaleTID -> SaleTable.ItemTID -> ItemTable.TID`

#### Scenario: Search by NPC for shop items
- Given 用户输入 NPC 名称或 NPC TID
- When 系统命中一个 NPC
- Then 系统返回该 NPC 通过 `SaleTID` 明确关联到的商店物品
- And 每条结果都显示来源链路

#### Scenario: Search by item for NPC shop sources
- Given 用户输入 Item 名称或 Item TID
- When 系统命中一个 Item
- Then 系统返回明确售卖该物品的 NPC
- And 系统不得因为无关 `TID` 数值碰撞而创建商店关系

#### Scenario: Numeric query matches both NPC and Item
- Given 用户输入一个纯数字
- And 该值同时命中 `NpcTable.TID` 与 `ItemTable.TID`
- When 系统执行查询
- Then 系统返回显式歧义结果
- And 系统要求用户细化查询
- And 系统不得静默偏向任一对象域

### Requirement: NPC drop relation query

系统 SHALL 支持基于以下高置信业务链路查询 NPC 掉落关系：

- `NpcTable.ItemDropTID -> ItemDropTable.TID -> ItemDropTable.DropItemXX -> ItemTable.TID`

#### Scenario: Search by NPC for drop items
- Given 用户输入 NPC 名称或 NPC TID
- When 系统命中一个 NPC
- Then 系统返回该 NPC 通过 `ItemDropTID` 明确关联到的掉落物品
- And 每条结果都显示对应 `DropItemXX` 来源

#### Scenario: Search by item for NPC drop sources
- Given 用户输入 Item 名称或 Item TID
- When 系统命中一个 Item
- Then 系统返回明确掉落该物品的 NPC
- And 系统不得把 `MapDropTID` / `ItemDropWorldTable` 自动升级为默认关系

### Requirement: Trust-first operator output

系统 MUST 以运营可核对的方式输出结果。每条关系 SHALL 至少包含：

- NPC 基础身份
- relation type（drop / shop）
- item 基础身份
- traceable source path
- trust status

#### Scenario: Missing or invalid relation ID
- Given 某 NPC 的 `SaleTID` 或 `ItemDropTID` 为 0、空值或无效引用
- When 系统执行查询
- Then 系统返回空关系而不是伪造结果

#### Scenario: Uncertain relation
- Given 某链路不在本次允许的高置信业务关系中
- When 系统执行查询
- Then 系统不得静默输出该关系为确定事实
