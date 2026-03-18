# operator_query_domains

## 目的

本文定义下一阶段运营向查询工具的**问题域（query domains）**，用于约束后续查询能力的产品边界。

核心原则不是“仓库里有哪些表”，而是“运营在处理问题时需要先查什么对象、再补什么关系”。

## 已确认前提

1. 当前 `item-query-v1` 已经收口，范围刻意保持在“仅物品查询 + 最小装备链路”。
2. 任何后续增强都应作为新 change 推进，而不是继续扩展现有 v1。
3. 现阶段产出的是**运营查询域模型**与**表白名单边界**，不是多业务域 UI 设计，也不是全表浏览器。

## 运营向问题域

### 1. Items / Drops / Shops（首要域）

这是最直接、最高频的运营排障入口，适合继续作为后续能力演进的主轴。

典型问题：

- 某个物品为什么没有按预期掉落？
- 哪个 NPC 会掉这个物品？
- 哪个商店会卖这个物品？
- 这个物品能开出什么、分解出什么、强化用什么、炼金/合成到什么？

该域的核心对象是：

- Item
- NPC drop
- Shop sale
- Item transformation / progression chain

### 2. Quests（第二优先域）

任务问题对运营同样高价值，但更适合作为“围绕物品/NPC的相邻域”，而不是直接做成全量任务百科。

典型问题：

- 某任务为什么不给预期道具？
- 某任务要打什么怪、收集什么道具、完成什么目标？
- 某任务的奖励和投放链路是否正确？
- 某物品/某 NPC 与哪些任务直接相关？

该域的核心对象是：

- Quest
- Mission
- Reward
- Quest-specific drop / give-item

### 3. NPCs（第二优先域）

NPC 是运营理解“谁掉落、谁售卖、谁触发任务”的关键锚点，适合成为独立主入口之一。

典型问题：

- 这个 NPC 掉什么？
- 这个 NPC 卖什么？
- 这个 NPC 是否参与某任务或某区域问题？

该域的核心对象是：

- NPC
- NPC drop reference
- NPC sale reference

### 4. World / Map / Area / Portal Guidance（导航上下文域）

这不是“全世界编辑器”，而是运营排障时需要的**导航上下文**。

典型问题：

- 某任务/NPC/入口大致位于哪个世界或区域？
- 某传送门会把玩家送到哪里？
- 某世界地点是否与任务或副本入口相关？

该域的核心对象是：

- World
- Map
- Area
- Portal
- WorldPlace

### 5. Events / Instances（后续扩展域）

这是合理的后续方向，但当前不建议作为第一批主入口。

原因：

- 运营价值存在，但排障路径通常仍需回到 item / quest / NPC / map 上下文。
- 语义复杂，容易把分析型工具再次拉向“全系统总览”。

适合作为 later expansion 的对象：

- Event
- Instance / instance reward / instance round

## 推荐的产品进入顺序

### 第一批主入口

1. Item
2. NPC
3. Quest

### 第一批上下文增强

1. Shop / sale
2. Drop
3. World / map / area / portal
4. Item transformation chain（box / break / enchant / alchemy / mix / socket / set）

### 明确后置

1. Event
2. Instance
3. 纯展示/UI/引擎支持表

## 查询产品边界

后续查询工具建议遵循以下边界：

- **允许**：围绕运营问题提供对象检索与高置信关系说明。
- **不允许**：把所有 CSV 表直接暴露成浏览器式入口。
- **不允许**：只因字段同名（如 `TID`）就宣称存在业务关系。
- **不允许**：把技术上可连通的数值碰撞当成实体同一性。

## 本文结论

下一阶段运营向查询工具，最合理的对象域模型是：

1. Item / Drop / Shop
2. Quest
3. NPC
4. World / Map / Area / Portal guidance
5. Event / Instance as later expansion

其中真正适合作为**主搜索入口**的，是 Item、NPC、Quest；World/Map 类更适合作为导航上下文增强，而 Event/Instance 暂缓进入默认主搜索空间。
