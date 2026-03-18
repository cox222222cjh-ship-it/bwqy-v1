# Spec: build-quest-query-v1

## ADDED Requirements

### Requirement: Quest query entry is QuestTable-only by default

系统 SHALL 只以 `QuestTable` 作为 Quest v1 的默认顶层查询入口。

#### Scenario: Search quest by TID
- Given 用户输入一个 Quest TID
- When `QuestTable.TID` 精确命中一个 Quest
- Then 系统返回该 Quest 作为主记录
- And 系统只解析本 spec 白名单中的 Quest 关系

#### Scenario: Search quest by name
- Given 用户输入一个 Quest 名称
- When 系统按 Quest 名称字段命中一个 Quest
- Then 系统返回该 Quest 作为主记录

#### Scenario: Multiple quests match by name
- Given 用户输入一个 Quest 名称
- When 系统命中多个 Quest
- Then 系统返回 `ambiguous` 状态
- And 系统列出候选 Quest 列表
- And 系统不得默认猜测第一条结果

### Requirement: Quest v1 relation scope is whitelist-only

系统 SHALL 只支持以下高置信 Quest 关系：

- `QuestTable.MissionTID -> QuestMissionTable.TID`
- `QuestTable.RewardTID -> QuestRewardTable.TID`
- `QuestDropTable.QuestTID = QuestTable.TID`
- `QuestTable.GiveItem1 -> ItemTable.TID`
- `QuestTable.GiveItem2 -> ItemTable.TID`
- `QuestTable.PrevQuest -> QuestTable.TID`
- `QuestTable.NextQuest -> QuestTable.TID`

#### Scenario: Return mission relation
- Given 某 Quest 的 `MissionTID` 命中 `QuestMissionTable.TID`
- When 查询该 Quest
- Then 系统返回 mission relation

#### Scenario: Return reward entries
- Given 某 Quest 的 `RewardTID` 命中一个或多个 `QuestRewardTable` 记录
- When 查询该 Quest
- Then 系统返回这些 reward entries
- And 系统保留 reward entry 的类型信息

#### Scenario: Return quest-specific drops
- Given `QuestDropTable.QuestTID = QuestTable.TID`
- When 查询该 Quest
- Then 系统返回对应的 quest-specific drop entries
- And 可在高置信情况下补充 NPC / Item 解释

#### Scenario: Return give items
- Given 某 Quest 的 `GiveItem1` 或 `GiveItem2` 命中 `ItemTable.TID`
- When 查询该 Quest
- Then 系统返回对应 give item entries

#### Scenario: Return prev and next quests
- Given 某 Quest 的 `PrevQuest` 或 `NextQuest` 命中 `QuestTable.TID`
- When 查询该 Quest
- Then 系统返回前置与后续 Quest

### Requirement: Quest v1 must preserve operator-facing exclusions

系统 SHALL 保持默认运营查询排除边界，不因 Quest v1 而放宽。

#### Scenario: Default-excluded tables are not auto-included
- Given 默认排除表如 `HelpTable`、`TutorialTable`、`BanWordTable`、`Char*`、`QuestCinemaTable`、`QuestSceneTable`
- When 用户执行 Quest v1 查询
- Then 这些表不会进入默认查询路径
- And 这些表不会出现在默认关系结果中

### Requirement: Quest v1 must not use full-table scan as product strategy

系统 SHALL NOT 通过遍历全仓 CSV 表寻找 Quest 关联来构建默认结果。

#### Scenario: Only whitelist tables are consulted
- Given 用户查询一个 Quest
- When 系统构建响应
- Then 系统只读取或索引 whitelist tables 和受控解释表
- And 系统不会从未列入白名单的表中自动补关系

### Requirement: Quest v1 must not auto-link by same-name `TID`

系统 SHALL NOT 因字段名称同为 `TID` 就自动推断存在 Quest 关系。

#### Scenario: Reward value is numeric but not proven item relation
- Given 一个 `QuestRewardTable` 记录包含数值型 `Value`
- And 当前证据不足以证明该值必然是 `ItemTable.TID`
- When 系统输出 reward relation
- Then 系统不得把该值当作 item 事实输出
- And 系统应保留原始 reward entry，并在必要时标记 `pending_confirmation`

#### Scenario: DropTID is not treated as sole truth if unstable
- Given `QuestTable.DropTID` 与 `QuestDropTable.TID` 的稳定性尚未被证明
- When 系统输出 quest drop relation
- Then 系统以 `QuestDropTable.QuestTID = QuestTable.TID` 作为主事实来源
- And `DropTID` 只能作为补充校验或待确认信息
