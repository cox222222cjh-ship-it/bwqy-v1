# Quest Query v1

## 范围

Quest Query v1 只允许从 `QuestTable` 进入，并且只展开以下白名单关系：

- `QuestTable.MissionTID -> QuestMissionTable.TID`
- `QuestTable.RewardTID -> QuestRewardTable.TID`
- `QuestDropTable.QuestTID = QuestTable.TID`
- `QuestTable.GiveItem1/2 -> ItemTable.TID`
- `QuestTable.PrevQuest/NextQuest -> QuestTable.TID`

## 默认排除

以下内容不进入 Quest v1 默认查询空间：

- `HelpTable`、`TutorialTable`、`TipTable`、`BanWordTable`、`Message*`
- `Char*`、`Customize*`、`Effect*`
- `QuestCinemaTable`、`QuestSceneTable`
- `WorldTable`、`MapTable`、`AreaTable`、`PortalTable`、`WorldPlaceTable`

## 响应结构

查询返回以下稳定形态：

- `status=ok`：返回单个 quest 与五类关系分区。
- `status=ambiguous`：返回候选 quest 列表。
- `status=not_found`：返回空 quest / payload，并附带说明 note。

单 quest 命中时，payload 包含：

- `prev_quest`
- `next_quest`
- `give_items`
- `missions`
- `rewards`
- `quest_drops`
- `related_items`
- `related_npcs`

向量字段的保守处理规则：

- `MissionTID` / `RewardTID` 若包含多个 ID，Quest v1 会按原始顺序逐个解析到既有 `missions` / `rewards` 列表。
- `PrevQuest` / `NextQuest` 仍保持单链接响应形态；若源字段包含多个有效 ID，结果会退化为保守的单条 `pending_confirmation` 解释，并额外写入 note。
- `DropTID` 会被安全解析，但始终只作为诊断信息，不会升级为 quest drop 主事实来源。

## 限制

- 不做跨域自动跳转到 Item / NPC 主入口。
- 不因 reward 的 `Value` 是数字就默认解释为 item。
- `QuestTable.DropTID` 与 `QuestDropTable.TID` 未被当作稳定一一关系；实现仅用其生成诊断 note。
- `PrevQuest`、`NextQuest`、`MissionTID`、`RewardTID`、`DropTID` 在底层 schema 中可为向量字段；Quest v1 对这些字段只做保守解释，不会把多值伪装成单一确定事实。

## 示例

```python
from item_query_v1.quest_query import build_quest_query_index, query_quest

index = build_quest_query_index()
result = query_quest(index, "哥布林的异常繁殖")

if result.status == "ok":
    print(result.payload.missions)
elif result.status == "ambiguous":
    print(result.candidates)
```
