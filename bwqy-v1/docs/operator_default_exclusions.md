# operator_default_exclusions

## 目的

本文定义默认不进入运营查询空间的表类型。

这里的“排除”并不表示这些表永远无用，而是表示：

- 不应成为默认主搜索入口；
- 不应被自动纳入通用关系扩展；
- 不应因为“也有 `TID`”就被查询工具默认暴露。

## 排除原则

满足以下任一条件，即应默认排除：

1. 纯 UI / 帮助 / 文案 / 教学支持。
2. 纯角色外观 / 定制 / 表现配置。
3. 纯特效 / 动画 / 渲染 / 环境支持。
4. 纯引擎参数 / 插值 / 地形 / 音效环境支持。
5. 对运营问题没有自然对象语义，或必须依附其它表才能解释。
6. 即使有业务相关性，也不足以进入当前默认运营搜索空间。

---

## 1. 明确默认排除的代表表

### A. 帮助 / 教学 / 提示 / 违禁词

- `HelpTable.csv`
- `TutorialTable.csv`
- `TipTable.csv`
- `BanWordTable.csv`
- `MessageTable.csv`
- `MessageBoxTable.csv`
- `ChatTable.csv`
- `CommandTable.csv`
- `MailTable.csv`

原因：

- 更偏运营公告/系统文本/规则支持，而不是运营排障的核心对象。

### B. 角色外观 / 模型 / 形象 / 自定义

- `CharShapeTable.csv`
- `CharFigureTable.csv`
- `CharBaseInfoTable.csv`
- `CustomizeTable.csv`
- `CustomizePreviewTable.csv`
- `PcTable.csv`
- `SummonTable.csv`
- `WarUniformTable.csv`

原因：

- 更偏角色表现或创建配置，不是默认运营问题域。

### C. 特效 / 动作 / 动画 / 武器表现

- `EffectEventTable.csv`
- `CharEffectTable.csv`
- `CharEffectTable_Sound.csv`
- `CharBlendAniTable.csv`
- `FixedDummyAniTable.csv`
- `ToolWeaponTable.csv`
- `WeaponAbilityTable.csv`

原因：

- 属于表现/引擎支持层，不适合默认暴露给运营查询工具。

### D. 引擎 / 环境 / 地形 / 插值支持

- `Interpolator.csv`
- `TerrainSurfaceTable.csv`
- `WeatherTable.csv`
- `WorldEnvLightTable.csv`
- `WorldEnvSoundTable.csv`
- `WorldEnvWaterTable.csv`
- `RandomNodeTable.csv`
- `NaviPointTable.csv`

原因：

- 即使与场景运行有关，也不是运营面向玩家问题时的首选对象。

### E. 系统/成长/战斗底层参数

- `LevelupTable.csv`
- `LevelCompareTable.csv`
- `PartyExpTable.csv`
- `StatTable.csv`
- `SkillBaseAttackTable.csv`
- `SkillComboTable.csv`
- `SkillLearnTable.csv`
- `SkillTable.csv`
- `WeaponLvTable.csv`
- `ProductLvTable.csv`

原因：

- 这类表更适合后续做专门的战斗/成长分析工具，而不是当前运营查询默认空间。

### F. 其它当前默认排除项

- `LocalizeTable.csv`
- `ContentsOptionTable.csv`
- `ServerInfoTable.csv`
- `TitleTable.csv`
- `GuildTable.csv`
- `FamePointTable.csv`
- `WarContentsTable.csv`
- `TriggerTable.csv`
- `QuestCinemaTable.csv`
- `QuestSceneTable.csv`
- `NpcBrainTable.csv`
- `NpcDlgStringTable.csv`
- `EntityTable.csv`
- `CashShopInfo.csv`
- `ItemCoinTable.csv`
- `ItemDropLimitTable.csv`
- `ItemMatrixTable.csv`
- `ItemEnchantGlowTable.csv`
- `ItemSeedTable.csv`
- `SaleTable.csv`（仅排除为主入口，不排除其 supporting relation 身份）
- `WorldMapUITable.csv`

原因：

- 有些是底层规则表，有些是辅助表，有些虽与业务有关但不适合做默认入口。

## 2. 特别说明：不是“无用”，而是“默认不暴露”

以下几类需要特别区分：

### supporting relation but not top-level

这些表不是默认主入口，但仍应在受控范围内使用：

- `SaleTable.csv`
- `ItemDropTable.csv`
- `QuestMissionTable.csv`
- `QuestRewardTable.csv`
- `QuestDropTable.csv`
- `WorldPlaceTable.csv`
- `ItemBoxTable.csv`
- `ItemBreakTable.csv`
- `ItemEnchantTable.csv`
- `ItemAlchemyTable.csv`
- `ItemMixTable.csv`
- `ItemSocketTable.csv`
- `ItemSetTable.csv`
- `ItemSetAbilityTable.csv`
- `ProductItemTable.csv`

这些表不应被误判为“排除后完全不用”，而是“只作为受控支撑表使用”。

### later expansion but not now

以下表有潜在运营价值，但不应进入当前默认搜索空间：

- `EventTable.csv`
- `InstanceMapTable.csv`
- `InstanceRewardTable.csv`
- `InstanceRoundTable.csv`

## 本文结论

默认运营搜索空间应明确排除：

- Help / Tutorial / BanWord / Tip / Message 等帮助文本类表；
- CharShape / CharFigure / Customize / CharEffect / Interpolator 等表现与引擎支持表；
- 大量成长、技能、环境、战斗底层参数表；
- 其它虽然技术上可读，但不符合运营自然查询对象的表。

后续查询工具必须坚持“默认少而准”，而不是从全仓库表清单反推产品入口。
