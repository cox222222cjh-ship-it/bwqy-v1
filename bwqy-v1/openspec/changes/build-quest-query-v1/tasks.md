# Tasks: build-quest-query-v1

## Task 1: Freeze Quest v1 scope

- 仅覆盖 Quest 主记录查询。
- 仅覆盖以下关系：
  - Quest -> Mission
  - Quest -> Reward
  - Quest -> QuestDrop
  - Quest -> GiveItem
  - Quest -> Prev/Next
- 明确 Quest v1 不是 full-table browser，也不是 quest encyclopedia。

## Task 2: Define source tables and allowed fields

- 冻结 top-level table：`QuestTable`。
- 冻结 supporting relation tables：`QuestMissionTable`、`QuestRewardTable`、`QuestDropTable`。
- 冻结受控解释表：`ItemTable`、`NpcTable`。
- 为每条关系列出唯一允许的连接字段，不允许 same-name `TID` auto-linking。

## Task 3: Define result model and ambiguity model

- 定义 Quest 基础身份字段。
- 定义 prev/next、give_items、missions、rewards、quest_drops 五个结果分区。
- 定义 `confirmed` / `missing` / `pending_confirmation` 三种关系状态。
- 定义 `ambiguous` / `not_found` 响应。

## Task 4: Build minimal read/index path

- Quest by `TID` / 名称。
- Mission by `QuestTable.MissionTID`。
- Reward entries by `QuestTable.RewardTID`。
- Quest drop entries by `QuestDropTable.QuestTID`。
- Give items by `QuestTable.GiveItem1/2`。
- Prev/Next by `QuestTable.PrevQuest/NextQuest`。

## Task 5: Add focused acceptance tests

至少覆盖：

- 单 quest 命中并返回五类关系分区。
- 名称多命中返回 `ambiguous`。
- `PrevQuest` / `NextQuest` / `GiveItem` 无效引用返回 `missing`。
- `QuestRewardTable.Value` 不得仅因是数字就自动映射为 item。
- `QuestDropTable.QuestTID` 生效时可返回 quest-specific drop。
- `DropTID` 不稳定时不会被当作唯一事实来源。
- 默认排除表不会进入 Quest v1 结果。
- 不会因其它表存在同名 `TID` 字段而产生自动关系。

## Task 6: Update operator-facing docs

- 记录 Quest v1 的白名单、排除项与可信关系。
- 说明 Quest v1 仍遵循 operator-oriented query-domain whitelist principle。
- 说明 Quest v1 与 item / NPC 现有边界的衔接方式。
