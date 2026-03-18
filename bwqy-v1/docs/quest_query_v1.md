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

## 限制

- 不做跨域自动跳转到 Item / NPC 主入口。
- 不因 reward 的 `Value` 是数字就默认解释为 item。
- `QuestTable.DropTID` 与 `QuestDropTable.TID` 未被当作稳定一一关系；实现仅用其生成诊断 note。

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
