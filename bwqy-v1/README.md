# item-query-v1（Task 5）本地运行说明

## 功能范围（v1）

当前实现严格按 OpenSpec Task 1~5 最小范围：

- 仅支持物品名称 / 物品 ID 查询
- 仅接入 `ItemTable`、`ItemSetTable`、`ItemSetAbilityTable`
- 查询结果基于 Task 4 结果视图模型渲染
- 仅提供本地只读 Web UI（无写操作、无网络依赖）

## 启动本地 Web UI

在仓库根目录下执行：

```bash
python -m item_query_v1.web_ui
```

默认监听：

- `http://127.0.0.1:8000`

## 页面行为

页面包含以下最小区域：

1. 查询输入区（一个输入框 + 一个查询按钮）
2. 单结果详情区（仅五个允许 section）
   - basic information
   - classification
   - source information
   - trust status
   - equipment chain
3. 候选结果区（多命中时展示候选列表，不强制进入详情页）
4. 无结果区
5. 错误区（索引加载失败 / 查询异常）

此外，`pending_confirmation` 会在页面中显式标识。

## 测试

运行：

```bash
python -m unittest discover -s tests
```


## Unified Operator Query Backend（最小统一后端入口）

当前仓库已提供一个**只读统一路由层**，用于把 Item / NPC / Quest 三个既有查询域收敛到一个稳定后端入口，便于后续 CLI / Web 集成。

入口能力：

- 接受一个原始查询字符串 `raw_query`
- 可选接受 `domain_hint`：`item` / `npc` / `quest`
- 在未提供 `domain_hint` 时，只在既有白名单域内做最小路由判断
- 输出稳定规范化 envelope：
  - `domain`
  - `status`
  - `primary_payload`
  - `notes`

规范化状态语义：

- `exact_match`：唯一稳定命中一个域
- `ambiguous`：命中冲突，或现有域逻辑要求显式细化
- `not_found`：三大白名单域都未命中

当前歧义规则：

- 纯数字若同时命中 `NpcTable.TID` 与 `ItemTable.TID`，直接返回 `ambiguous`
- 名称若跨 Item / Quest 等多个主域同时稳定命中，也返回 `ambiguous`
- 若某一域自身已返回多候选（例如 item 重名），统一层保留该域的歧义状态，不替该域做低置信猜测

当前统一层**不会**做的事情：

- 不做 full-table scanning 作为产品策略
- 不做 same-name `TID` 自动联表
- 不做低置信关系推断
- 不扩展 world / map / navigation 域
- 不改变现有 item / npc / quest 领域内部白名单边界

示例：

```python
from item_query_v1.unified_query_service import (
    build_unified_query_router_index,
    route_operator_query,
)

index = build_unified_query_router_index()
result = route_operator_query(index, "QUEST_EXACT")
```

## 收口说明

- 详见 `docs/v1-closure.md`，用于记录本次 v1 最终核验、已知限制与后续变更边界。

## NPC 掉落 / 商店最小运营查询

当前仓库另外提供了一个**代码级最小查询能力**，用于运营核对 NPC 与 item 的 drop/shop 关系。

支持的输入：

- NPC 名称 / NPC TID
- Item 名称 / Item TID

数字输入的安全规则：

- 如果一个纯数字同时命中 `NpcTable.TID` 和 `ItemTable.TID`，系统会返回显式歧义结果，不会默认猜成 NPC 或 Item。
- 此时应改用名称，或补充更明确的对象上下文再查询。

支持的输出：

- 这个 NPC 卖什么
- 这个 NPC 掉什么
- 哪些 NPC 卖这个物品
- 哪些 NPC 掉这个物品

仅包含的表与关系：

- `NpcTable.SaleTID -> SaleTable.SaleTID -> SaleTable.ItemTID -> ItemTable.TID`
- `NpcTable.ItemDropTID -> ItemDropTable.TID -> ItemDropTable.DropItemXX -> ItemTable.TID`

明确暂不包含：

- Quest
- `MapDropTID` / `ItemDropWorldTable`
- broad full-table search

示例：

```python
from item_query_v1.npc_shop_drop_query import build_npc_shop_drop_index, query_npc_or_item

index = build_npc_shop_drop_index()
result = query_npc_or_item(index, "NPC_NAME_OR_ITEM_NAME")
```


## Quest Query v1（最小运营闭环）

当前仓库另外提供了一个**代码级最小 Quest 查询能力**，严格遵循 `build-quest-query-v1` 的白名单边界。

支持的输入：

- Quest TID
- Quest `LocalTitle`

稳定输出结构覆盖：

- exact quest match
- name search `ambiguous` candidates
- related items / related NPCs
- prev / next quest links
- not found / missing / pending confirmation

仅包含的表与关系：

- 顶层入口：`QuestTable`
- supporting relation：`QuestMissionTable`、`QuestRewardTable`、`QuestDropTable`
- controlled interpretation：`ItemTable`、`NpcTable`
- 高置信关系：
  - `QuestTable.MissionTID -> QuestMissionTable.TID`
  - `QuestTable.RewardTID -> QuestRewardTable.TID`
  - `QuestDropTable.QuestTID = QuestTable.TID`
  - `QuestTable.GiveItem1/2 -> ItemTable.TID`
  - `QuestTable.PrevQuest/NextQuest -> QuestTable.TID`

明确限制：

- 不做 full-table browser。
- 不因同名 `TID` 自动联表。
- `QuestTable.DropTID` 只作补充诊断，不作 quest drop 主事实来源。
- `PrevQuest`、`NextQuest`、`MissionTID`、`RewardTID`、`DropTID` 属于向量型字段时，Quest v1 会保守处理：`MissionTID` / `RewardTID` 按顺序展开，`PrevQuest` / `NextQuest` 仅保留降阶后的单链接解释并标记待确认。
- 不默认纳入 `HelpTable`、`TutorialTable`、`BanWordTable`、`Char*`、`QuestCinemaTable`、`QuestSceneTable`、world/map/navigation 表。

示例：

```python
from item_query_v1.quest_query import build_quest_query_index, query_quest

index = build_quest_query_index()
result = query_quest(index, "1")
```
