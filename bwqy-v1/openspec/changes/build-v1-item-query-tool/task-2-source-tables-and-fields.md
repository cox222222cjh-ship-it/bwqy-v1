# Task 2 - Define Source Tables and Fields（主表与字段定义）

## 1) 输入数据现状（基于已上传 table）

当前仓库数据目录 `data/tables/` 已包含 `data/tables/ItemTable.csv`、`data/tables/ItemSetTable.csv`、`data/tables/ItemSetAbilityTable.csv` 等表。

观察到这些 CSV 结构均包含“说明行/空行/类型行”，典型模式为：

- 第 1 行：字段名（Header）
- 第 2 行：中文说明
- 第 3 行：空行
- 第 4 行：字段类型
- 第 5 行开始：真实业务数据

因此 v1 读取规则必须固定为：**将第 2~4 行视为元信息并跳过，只从第 5 行起解析业务记录**。

## 2) v1 主表与最小关联表清单

### 2.1 主表（可信锚点）

- `data/tables/ItemTable.csv`
- 主键：`TID`

### 2.2 装备链路最小关联表（仅一条高确定性链路）

- `data/tables/ItemSetTable.csv`
  - 作用：由套装/物品关系连接 `ItemTID` 与 `SetAbilityTID`
- `data/tables/ItemSetAbilityTable.csv`
  - 作用：给出套装能力触发条件（`ReqTotal`）与说明（`LocalDesc`）

> 说明：v1 不引入 `data/tables/ItemEnchantTable.csv`、`data/tables/ItemBreakTable.csv`、`data/tables/ProductItemTable.csv` 等更复杂链路，避免范围失控。

## 3) 字段职责划分

## 3.1 搜索字段（MUST）

- `ItemTable.TID`：ID 精确查询。
- `ItemTable.LocalName`：名称查询主字段。
- `ItemTable.EngName`：名称查询辅助字段（英文键）。

## 3.2 基础信息字段（直接展示）

- `ItemTable.TID`
- `ItemTable.LocalName`
- `ItemTable.EngName`
- `ItemTable.Level`
- `ItemTable.Grade`
- `ItemTable.Race`
- `ItemTable.Gender`
- `ItemTable.StackCount`
- `ItemTable.MaxCount`
- `ItemTable.LocalDesc`

## 3.3 分类字段

### 直接读取（可稳定展示）

- `ItemTable.Type`
- `ItemTable.Kind`
- `ItemTable.Property`

### 推断（可展示但要标记为“推断”）

- `is_equipment`（是否装备）
  - v1 规则：
    - 当 `SetTID > 0`，或存在装备属性字段非零（如 `AP/DP/BP/CP`）时，判为“可能装备”。
    - 否则判为“非装备或未知”。
  - 原因：当前未见稳定字典将 `Type/Kind` 数值严格映射到“装备/非装备”业务语义。

### 待确认

- `category_name_zh`（中文分类名）
  - 原因：缺少官方、可验证的 `Type/Kind/Property` 编码字典。

## 3.4 装备链路字段（最关键链路）

v1 仅定义“套装链路”：

1. `ItemTable.SetTID`（主表直接字段）
2. `ItemSetTable.TID`（套装主键）
3. `ItemSetTable.ItemTID`（套装包含的物品 TID 列表）
4. `ItemSetTable.SetAbilityTID`（能力 TID 列表）
5. `ItemSetAbilityTable.TID`
6. `ItemSetAbilityTable.ReqTotal`
7. `ItemSetAbilityTable.LocalDesc`

## 4) 字段状态分级（展示侧强制）

每个展示项必须带以下元信息：

- `source_table`
- `source_field`
- `status`（直接读取 / 推断 / 待确认）
- `note`（可选，记录推断规则或待确认原因）

## 5) v1 可直接展示字段白名单

以下字段可在 v1 作为“直接读取”输出（无需推断）：

- 主表基础：`TID`、`LocalName`、`EngName`、`Level`、`Grade`、`Type`、`Kind`、`Property`、`SetTID`、`LocalDesc`
- 套装链路：`ItemSetTable.TID`、`ItemSetTable.ItemTID`、`ItemSetTable.SetAbilityTID`
- 套装能力：`ItemSetAbilityTable.TID`、`ItemSetAbilityTable.ReqTotal`、`ItemSetAbilityTable.LocalDesc`

## 6) v1 必须标记“待确认”的字段/能力

1. 中文分类名（`Type/Kind/Property` 的中文业务名）
2. 装备大类名称（如“武器/防具/饰品”）
3. 非套装装备的完整成长链路（强化、分解、炼金、合成等）
4. 任意跨表但无法给出确定连接依据的关联结果

## 7) 输出示例（展示模型）

```json
{
  "label": "物品名称",
  "value": "艾林河鞋(更快速)",
  "source_table": "ItemTable",
  "source_field": "LocalName",
  "status": "直接读取"
}
```

```json
{
  "label": "是否装备",
  "value": "可能是",
  "source_table": "ItemTable",
  "source_field": "SetTID|AP|DP|BP|CP",
  "status": "推断",
  "note": "依据 v1 装备判定规则，缺少官方分类字典"
}
```

```json
{
  "label": "装备分类中文名",
  "value": "待确认",
  "source_table": "ItemTable",
  "source_field": "Type|Kind|Property",
  "status": "待确认",
  "note": "缺少可验证编码字典"
}
```
