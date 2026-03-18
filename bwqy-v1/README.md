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
## 收口说明

- 详见 `docs/v1-closure.md`，用于记录本次 v1 最终核验、已知限制与后续变更边界。

## NPC 掉落 / 商店最小运营查询

当前仓库另外提供了一个**代码级最小查询能力**，用于运营核对 NPC 与 item 的 drop/shop 关系。

支持的输入：

- NPC 名称 / NPC TID
- Item 名称 / Item TID

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
