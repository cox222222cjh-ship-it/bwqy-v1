# operator_table_whitelist

## 目的

本文给出运营向查询工具的表白名单模型，将表拆分为：

1. 顶层可搜索表（Top-level searchable tables）
2. Supporting relation tables
3. 不纳入本文；默认排除表见 `docs/operator_default_exclusions.md`

## 判定标准

只有同时满足以下条件的表，才应进入默认运营搜索空间：

1. 能对应运营真实问题中的“对象”。
2. 字段语义足够稳定，能被非开发角色理解。
3. 与其它白名单表之间存在高置信、业务可解释的关系。
4. 不是纯 UI、纯引擎、纯表现配置。

---

## 1. Top-level searchable tables

这些表可作为运营主动输入查询时的主入口。

### A. Item domain

- `ItemTable.csv`
  - 角色：物品主实体，是后续掉落、售卖、任务发放、物品链路的核心锚点。
  - 原因：已是 v1 已验证入口，且仍是运营最高频排障入口。

### B. NPC domain

- `NpcTable.csv`
  - 角色：NPC 主实体。
  - 原因：承载掉落（`ItemDropTID`）、地图掉落（`MapDropTID`）、商店（`SaleTID`）等运营高价值线索。

### C. Quest domain

- `QuestTable.csv`
  - 角色：任务主实体。
  - 原因：可直接回答任务标题、任务前后关系、任务目标组、奖励组、掉落组、GiveItem 等问题。

### D. Navigation / world context domain

以下表可进入主搜索空间，但建议在 UI 上弱于 Item/NPC/Quest：

- `WorldTable.csv`
  - 角色：世界主实体。
- `MapTable.csv`
  - 角色：地图主实体。
- `AreaTable.csv`
  - 角色：区域主实体。
- `PortalTable.csv`
  - 角色：传送门/跳转入口实体。

说明：

- 这些表属于“运营导航上下文”入口，不是配置百科入口。
- `WorldPlaceTable.csv` 暂不建议直接作为顶层搜索入口，因其更像导航关联节点而非运营自然查询对象。

---

## 2. Supporting relation tables

这些表应主要用于**丰富顶层对象详情**，不建议默认作为独立主搜索入口。

### A. Item supporting relations

- `ItemSetTable.csv`
  - 支撑 Item -> Set relation。
- `ItemSetAbilityTable.csv`
  - 支撑 Set -> Ability description。
- `ItemDropTable.csv`
  - 支撑 NPC -> drop group / Item <- dropped by NPC。
- `ItemDropWorldTable.csv`
  - 支撑世界掉落/活动掉落补充说明；优先作为补充来源，不单独开入口。
- `SaleTable.csv`
  - 支撑 NPC -> shop inventory / Item <- sold by NPC。
- `ItemBoxTable.csv`
  - 支撑 Item -> box contents。
- `ItemBreakTable.csv`
  - 支撑 Item -> break results。
- `ItemEnchantTable.csv`
  - 支撑 Item -> enchant group/step。
- `ItemAlchemyTable.csv`
  - 支撑 Item -> alchemy output / materials。
- `ItemMixTable.csv`
  - 支撑 Item -> mix recipe / result。
- `ItemSocketTable.csv`
  - 支撑 Item -> socket rule。
- `ProductItemTable.csv`
  - 支撑 Item -> production/crafting relation；仅作补充，不默认放主入口。

### B. Quest supporting relations

- `QuestMissionTable.csv`
  - 支撑 Quest -> mission objectives。
- `QuestRewardTable.csv`
  - 支撑 Quest -> reward entries。
- `QuestDropTable.csv`
  - 支撑 Quest -> quest-specific NPC/item drop relation。

### C. Navigation supporting relations

- `WorldPlaceTable.csv`
  - 支撑 Portal / world placement / quest or entity location context。
  - 不建议作为默认主入口，因为它更像中间定位节点。

### D. Later-expansion supporting relations

以下表可保留为后续扩展储备，但默认不放入当前主入口：

- `EventTable.csv`
- `InstanceMapTable.csv`
- `InstanceRewardTable.csv`
- `InstanceRoundTable.csv`

理由：

- 这些表有运营价值，但更适合作为第二阶段扩展域。
- 如果现在就放入默认主入口，会稀释第一批对象模型并拉大解释成本。

## 3. 不应纳入顶层入口的判断样式

即使某表“看起来和业务有关”，只要符合以下情况，也不应自动成为顶层搜索入口：

- 更像关系组/规则组，而不是运营自然会直接搜索的对象。
- 需要依附 Item/NPC/Quest 才有意义。
- 字段过于技术化，直接暴露给运营会增加误读风险。

典型例子：

- `SaleTable.csv` 更适合作为 “NPC 的商店商品列表” 支撑表，而不是让运营直接搜 `SaleTID`。
- `QuestMissionTable.csv` 更适合作为 “任务详情中的目标列表”。
- `ItemDropTable.csv` 更适合作为 “NPC 掉落组详情”。

## 本文结论

默认运营查询空间的**主入口表**应收敛为：

- `ItemTable.csv`
- `NpcTable.csv`
- `QuestTable.csv`
- `WorldTable.csv`
- `MapTable.csv`
- `AreaTable.csv`
- `PortalTable.csv`

其中最核心的前三项仍是：

- `ItemTable.csv`
- `NpcTable.csv`
- `QuestTable.csv`

其余白名单表主要承担详情补充、上下文导航、链路解释作用。
