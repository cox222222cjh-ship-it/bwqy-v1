# operator_strong_relations

## 目的

本文只记录**高置信、业务有意义**的关系白名单。

约束：

- 不因同名字段（尤其是 `TID`）自动认定存在关系。
- 不把跨表数值碰撞当成实体同一性。
- 只有当字段名和业务语义都足够清晰时，才纳入强关系。

---

## 1. Item-centered relations

### 1.1 Item -> ItemSet -> ItemSetAbility

关系链：

- `ItemTable.SetTID`
- `ItemSetTable.TID`
- `ItemSetTable.SetAbilityTID`
- `ItemSetAbilityTable.TID`

业务意义：

- 回答“该装备属于哪个套装、触发什么套装能力”。

可信度说明：

- 这是 v1 已采用的最小高置信装备链路，可继续保留。

### 1.2 Item -> Box contents

关系链：

- `ItemTable.BoxTID`
- `ItemBoxTable.TID`
- `ItemBoxTable.BoxItemXX`

业务意义：

- 回答“这个物品打开后可能产出什么”。

### 1.3 Item -> Break results

关系链：

- `ItemTable.BreakTID`
- `ItemBreakTable.TID`
- `ItemBreakTable.BreakItemXX`

业务意义：

- 回答“这个物品分解后可能得到什么”。

### 1.4 Item -> Enchant rule group

关系链：

- `ItemTable.EnchantTID`
- `ItemEnchantTable.GroupTID`

业务意义：

- 回答“该物品使用哪个强化规则组”。

待确认边界：

- `ItemEnchantTable.TID` 是步骤级记录，是否需要进一步解释为完整强化路径，应在后续特性里单独定义。

### 1.5 Item -> Alchemy rule

关系链：

- `ItemTable.AlchemyTID`
- `ItemAlchemyTable.TID`

业务意义：

- 回答“该物品关联哪条炼金规则；炼金可产出什么/需要什么材料”。

### 1.6 Item -> Mix rule

关系链：

- `ItemTable.MixTID`
- `ItemMixTable.TID`

业务意义：

- 回答“该物品关联哪条合成/混合规则”。

### 1.7 Item -> Socket rule

关系链：

- `ItemTable.SocketTID`
- `ItemSocketTable.TID`

业务意义：

- 回答“该物品使用哪条镶嵌规则”。

### 1.8 Item -> Product / crafting support

关系链：

- `ProductItemTable.ItemTID`
- `ItemTable.TID`
- `ProductItemTable.CompleteItemTID`
- `ItemTable.TID`

业务意义：

- 回答“该物品可作为生产材料，或是生产产物”。

约束：

- 这是明确字段语义的 relation，可进入白名单。
- 但 `ProductItemTable` 本身不建议成为默认主入口。

### 1.9 Item <- sold by NPC

关系链：

- `NpcTable.SaleTID`
- `SaleTable.SaleTID`
- `SaleTable.ItemTID`
- `ItemTable.TID`

业务意义：

- 回答“哪个 NPC 的商店售卖这个物品”。

说明：

- 这里以 `SaleTID` 作为业务桥，而不是因为各表都有 `TID` 就乱连。

### 1.10 Item <- dropped by NPC

关系链：

- `NpcTable.ItemDropTID`
- `ItemDropTable.TID`
- `ItemDropTable.DropItemXX`
- `ItemTable.TID`

业务意义：

- 回答“哪个 NPC 掉这个物品”。

说明：

- `NpcTable.MapDropTID` 与 `ItemDropWorldTable` 的业务意义可能有关，但当前字段名不足以单独确认完整链路，因此只作为补充上下文，不升级为默认强关系。

---

## 2. Quest-centered relations

### 2.1 Quest -> Mission

关系链：

- `QuestTable.MissionTID`
- `QuestMissionTable.TID`

业务意义：

- 回答“任务目标是什么、涉及什么 item/world position”。

### 2.2 Quest -> Reward

关系链：

- `QuestTable.RewardTID`
- `QuestRewardTable.TID`

业务意义：

- 回答“任务奖励是什么”。

待确认边界：

- `QuestRewardTable.Value` 的具体语义受 `Type` 影响，解释层仍应按类型区分，而不是直接一概视作 Item。

### 2.3 Quest -> Quest-specific drop

关系链：

- `QuestTable.DropTID`
- `QuestDropTable.QuestTID` 或直接以 `QuestDropTable.QuestTID = QuestTable.TID` 校验

业务意义：

- 回答“该任务要求或触发的专属掉落是什么，由哪个 NPC 掉”。

说明：

- `QuestTable.DropTID` 与 `QuestDropTable.TID` 是否始终一一对应，当前仍建议标注“待确认”。
- 但 `QuestDropTable.QuestTID`、`NpcTID`、`ItemTID` 的业务含义足够清晰，可纳入强关系白名单。

### 2.4 Quest -> Give items

关系链：

- `QuestTable.GiveItem1`
- `QuestTable.GiveItem2`
- `ItemTable.TID`

业务意义：

- 回答“任务开始或流程中直接给了什么物品”。

### 2.5 Quest -> predecessor / successor

关系链：

- `QuestTable.PrevQuest`
- `QuestTable.NextQuest`
- `QuestTable.TID`

业务意义：

- 回答“任务前置/后续关系”。

---

## 3. NPC-centered relations

### 3.1 NPC -> Drop group

关系链：

- `NpcTable.ItemDropTID`
- `ItemDropTable.TID`

业务意义：

- 回答“NPC 绑定哪条掉落组”。

### 3.2 NPC -> Shop inventory

关系链：

- `NpcTable.SaleTID`
- `SaleTable.SaleTID`

业务意义：

- 回答“NPC 使用哪套商店清单”。

### 3.3 NPC -> Quest drop entry

关系链：

- `QuestDropTable.NpcTID`
- `NpcTable.TID`

业务意义：

- 回答“这个 NPC 是否承担某个任务专属掉落”。

---

## 4. World / Map / Area / Portal relations

### 4.1 Map -> World

关系链：

- `MapTable.WorldTID`
- `WorldTable.TID`

业务意义：

- 回答“地图属于哪个世界”。

### 4.2 Area -> World

关系链：

- `AreaTable.WorldTID`
- `WorldTable.TID`

业务意义：

- 回答“区域属于哪个世界”。

### 4.3 WorldPlace -> World

关系链：

- `WorldPlaceTable.WorldTID`
- `WorldTable.TID`

业务意义：

- 作为位置节点时，回答“该世界位置隶属哪个世界”。

### 4.4 Portal -> WorldPlace

关系链：

- `PortalTable.DstWorldPlaceTID`
- `WorldPlaceTable.TID`

业务意义：

- 回答“该传送门把玩家送到哪个世界位置节点”。

待确认边界：

- `PortalTable.SrcEntityTID` / `DstEntityTID` 是否可稳定映射到某具体实体表，当前资料不足，不应默认升级为强关系。

### 4.5 Quest mission -> World

关系链：

- `QuestMissionTable.WorldTID`
- `WorldTable.TID`

业务意义：

- 回答“该任务目标发生在哪个世界”。

---

## 5. Later-expansion relations（只做储备，不进入默认关系集）

以下关系具有潜力，但当前不建议进入默认运营关系白名单：

- `QuestTable.EventTID` -> `EventTable.TID`
- `InstanceMapTable.ReqItem` -> `ItemTable.TID`
- `InstanceRewardTable` / `InstanceRoundTable` 相关链路
- `NpcTable.MapDropTID` 与世界掉落/活动掉落之间的进一步映射

原因：

- 字段存在，但默认产品价值、解释成本、稳定性还未收敛。
- 应在未来单独做 event / instance change 时再细化。

## 本文结论

下一阶段只应实现“高置信业务关系白名单”，重点围绕：

- Item -> drop / shop / box / break / enchant / alchemy / mix / socket / set
- Quest -> mission / reward / quest drop / give item / prev-next
- NPC -> drop / shop
- World / map / area / portal / world place 作为导航上下文

任何只因同名 `TID` 可连接的关系，都不应自动纳入默认查询工具。
