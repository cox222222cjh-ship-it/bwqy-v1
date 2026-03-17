# item-query-v1（Task 3）开发说明

## CSV 加载路径

Task 3 的本地读取逻辑会从当前代码位置向上查找 `data/tables` 目录，命中后作为 CSV 根路径。
在当前仓库结构下，实际路径为：

- `data/tables/ItemTable.csv`
- `data/tables/ItemSetTable.csv`
- `data/tables/ItemSetAbilityTable.csv`

## v1 已纳入表

仅包含 OpenSpec Task 2 约束的最小集合：

1. `ItemTable.csv`（可信锚点）
2. `ItemSetTable.csv`（套装关联）
3. `ItemSetAbilityTable.csv`（套装能力）

并严格按规则跳过 CSV 第 2~4 行元信息，从第 5 行开始解析业务记录。

## 已建立的最小索引

- `ItemTable.TID` 的精确索引（ID 查询）
- `ItemTable.LocalName` 的名称索引（主名称查询）
- `ItemTable.EngName` 的辅助名称索引（英文键）

## 返回结果结构（Task 3）

当前返回原始可追溯结构，供 Task 4 继续做展示映射：

- 字段级来源：`source_table`、`source_field`
- 字段原值：`raw_value`
- 字段状态：`direct | derived | pending_confirmation`

Task 3 里，直接从 CSV 读到的字段统一标记为 `direct`。

## 明确未实现（超出 v1 Task 3 范围）

- UI / 页面渲染
- Task 4 结果展示模型的最终渲染适配
- Task 5 Web 界面
- 任务、礼包、强化链路、全量多域入口
- 任意网络依赖或写回数据操作
- 除上述三张表外的其他 CSV 扩展接入
