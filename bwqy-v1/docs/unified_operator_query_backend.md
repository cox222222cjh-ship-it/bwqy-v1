# unified_operator_query_backend

## 目的

本文说明当前最小统一后端入口如何在 **Item / NPC / Quest** 三个既有运营查询域之上提供一个稳定、只读、可测试的服务层。

该层的目标不是替换现有领域模块，而是为未来 CLI / Web 集成提供一个共同后端契约。

## 统一入口支持内容

统一入口模块：`item_query_v1.unified_query_service`

支持：

- 输入一个 `raw_query`
- 可选输入 `domain_hint`
- 在白名单域内做最小路由
- 返回规范化响应 envelope

当前 `domain_hint` 可取：

- `item`
- `npc`
- `quest`

## 规范化响应契约

统一响应最小结构：

```python
UnifiedQueryResponse(
    query: str,
    domain: "item" | "npc" | "quest" | None,
    status: "exact_match" | "ambiguous" | "not_found",
    primary_payload: UnifiedQueryPayload | None,
    notes: list[str],
)
```

字段含义：

- `domain`
  - 当前统一层判定的主域
  - 若跨域歧义未消解，则为 `None`
- `status`
  - `exact_match`：唯一稳定命中
  - `ambiguous`：需要用户显式细化
  - `not_found`：当前白名单域都未命中
- `primary_payload`
  - 保留该域的主记录与原始领域结果，供后续上层做二次渲染
- `notes`
  - 用于输出歧义原因、约束提醒、保守解释说明

## 路由规则

### 1. 显式域优先

若调用方给出 `domain_hint`，统一层直接委派到对应领域模块：

- `item` -> `query_item`
- `npc` -> `query_npc_or_item`
- `quest` -> `query_quest`

这保证未来 CLI / Web 可以在交互上做“先域后查”的稳定模式。

### 2. 未显式给域时的最小自动路由

统一层会并行咨询三个既有领域模块，然后按保守策略做决策：

1. 若 NPC 模块先报告“数字同时命中 NPC 与 Item”，直接返回 `ambiguous`
2. 若只有一个主域给出稳定精确命中，返回该域
3. 若多个主域同时稳定命中，返回 `ambiguous`
4. 若三个主域都未命中，返回 `not_found`

## 当前保留的领域特性

统一层不会抹平既有领域差异，只做最小规范化：

### Item domain

仍保留：

- `TID` / `LocalName` / `EngName` 的命中逻辑
- 单命中与多候选区分
- 既有 set chain 行为

### NPC domain

仍保留：

- `NPC -> shop/drop -> item`
- `Item -> NPC shop/drop source`
- 纯数字命中 NPC TID 与 Item TID 时必须显式歧义

### Quest domain

仍保留：

- Quest 主记录优先
- mission / reward / quest drop / give item / prev-next 五类分区
- reward / vector link 等待确认策略

## 歧义规则

统一层当前只使用高置信歧义规则：

1. **数字域碰撞歧义**
   - 纯数字同时命中 NPC 和 Item 时，不自动偏向任一域
2. **跨主域名称碰撞歧义**
   - 如果同一名称在多个主域都形成稳定命中，则要求调用方显式给域
3. **域内多候选歧义**
   - 若 Item 或 Quest 域自身返回候选列表，统一层保留其 `ambiguous`，不代替用户猜测

## 明确不做

- 不做 full-table scanning 作为产品策略
- 不做 same-name `TID` auto-linking
- 不做低置信 relation inference
- 不改变现有 whitelist boundaries
- 不扩展到 map / world / navigation 域
- 不承担 UI 表现层职责

## 测试范围

统一层当前增加了以下 focused tests：

- item exact lookup
- npc exact lookup
- quest exact lookup
- ambiguous numeric input
- not_found behavior
- routing behavior across domains
- explicit domain hint behavior

## 后续可接入方向

后续 CLI / Web 若要复用该层，建议：

1. 使用 `domain_hint` 作为第一优先控制参数
2. 直接消费 `UnifiedQueryResponse`
3. 将 `primary_payload.result` 继续交给领域专用 formatter / presenter

这样可以保持统一入口稳定，同时保留各领域已有的可信边界。
