# 表级主键候选分析

- 说明：只统计字段名命中 `TID`、`*ID`、`*TID` 的列。
- 判定口径：`表内唯一`=非空值严格唯一；`高唯一但非严格唯一`=接近唯一但仍有少量重复；其余归为明显重复。

## ActionTable

- 文件：`data/tables/ActionTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：22
- 解析后的业务数据行数：18
- 字段总数：8
- 字段列表：TID, EngName, LocalName, Type, SkillTID, Icon, EndType, Desc

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 18 | 18 | 0 | 0 | 表内唯一（可疑似主键） |
| `SkillTID` | 100.00% | 18 | 18 | 0 | 0 | 表内唯一（可疑似主键） |

## AreaTable

- 文件：`data/tables/AreaTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：1428
- 解析后的业务数据行数：1424
- 字段总数：23
- 字段列表：TID, Type, Kind, WeatherUse, WorldTID, GroupNum, D_X, D_Y, D_Z, Radius, AimRebirthPos, DemolRebirthPos, Comment, EngName, EngSubName, LocalName, LocalSubName, BgmName, BgmLoop, Weather0, Weather1, Weather2, Weather3

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 1424 | 1424 | 0 | 0 | 表内唯一（可疑似主键） |
| `WorldTID` | 100.00% | 1424 | 155 | 75 | 1269 | 明显重复（不能当主键） |

## BanWordTable

- 文件：`data/tables/BanWordTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：2827
- 解析后的业务数据行数：2823
- 字段总数：3
- 字段列表：TID, Type, String

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 2823 | 2823 | 0 | 0 | 表内唯一（可疑似主键） |

## CashShopInfo

- 文件：`data/tables/CashShopInfo.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：154
- 解析后的业务数据行数：150
- 字段总数：10
- 字段列表：TID, VER, Type, SubType, ItemId, ItemNum, OnceNum, CastType, CastNum, Discount

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 150 | 150 | 0 | 0 | 表内唯一（可疑似主键） |
| `ItemId` | 100.00% | 150 | 150 | 0 | 0 | 表内唯一（可疑似主键） |

## CharBaseInfoTable

- 文件：`data/tables/CharBaseInfoTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：12
- 解析后的业务数据行数：8
- 字段总数：40
- 字段列表：TID, Race, Gen, MapID, Weapon_Shield, Weapon_Lance, Weapon_Staff, Weapon_Axe, Weapon_Bow, Weapon_Charkram, Weapon_Cannon, Weapon_Dagger, Weapon_Orb, Weapon_MagicGun, Weapon_Sword, Weapon_Blade, Weapon_Arbalest, Weapon_Wand, Skill_Shield, Skill_Lance, Skill_Staff, Skill_Axe, Skill_Bow, Skill_Charkram, Skill_Cannon, Skill_Dagger, Skill_Orb, Skill_MagicGun, Skill_Sword, Skill_Blade, Skill_Arbalest, Skill_Wand, StartLV, StartWLV, StartItem, StartItemCnt, StartItemQuick, ArchLordSkill, LimitAS, LimitRS

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 8 | 8 | 0 | 0 | 表内唯一（可疑似主键） |
| `MapID` | 100.00% | 8 | 1 | 1 | 7 | 明显重复（不能当主键） |

## CharBlendAniTable

- 文件：`data/tables/CharBlendAniTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：12
- 解析后的业务数据行数：8
- 字段总数：6
- 字段列表：TID, Priority, Weight, EaseInTime, Deactivate, Desc

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 8 | 8 | 0 | 0 | 表内唯一（可疑似主键） |

## CharEffectTable

- 文件：`data/tables/CharEffectTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：25370
- 解析后的业务数据行数：25366
- 字段总数：22
- 字段列表：CharName, Kind, EffectName, ResourceName, NodeName, SequenceID, StartTime, TimeLength, TX, TY, TZ, RX, RY, RZ, Scale, Flags, ActiveMode, DeActiveMode, DirMode, ActiveEvent, DeActiveEvent, Extend

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `SequenceID` | 100.00% | 25366 | 388 | 385 | 24978 | 明显重复（不能当主键） |

## CharEffectTable_Sound

- 文件：`data/tables/CharEffectTable_Sound.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：17806
- 解析后的业务数据行数：17802
- 字段总数：22
- 字段列表：CharName, Kind, EffectName, ResourceName, NodeName, SequenceID, StartTime, TimeLength, TX, TY, TZ, RX, RY, RZ, Scale, Flags, ActiveMode, DeActiveMode, DirMode, ActiveEvent, DeActiveEvent, Extend

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `SequenceID` | 100.00% | 17802 | 301 | 295 | 17501 | 明显重复（不能当主键） |

## CharFigureTable

- 文件：`data/tables/CharFigureTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：69
- 解析后的业务数据行数：65
- 字段总数：4
- 字段列表：TID, CharID, Name, BoneList

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 65 | 65 | 0 | 0 | 表内唯一（可疑似主键） |
| `CharID` | 100.00% | 65 | 9 | 8 | 56 | 明显重复（不能当主键） |

## CharShapeTable

- 文件：`data/tables/CharShapeTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：962
- 解析后的业务数据行数：958
- 字段总数：23
- 字段列表：ID, MediaPath, Bone, MPartsFace, MPartsEyeball, MPartsHair, MPartsHelm, MPartsBody, MPartsHand, MPartsLegs, MPartsFoot, MPartsCape, LHandWeapon, RHandWeapon, ItemMeshScale, StepLOD_01, StepLOD_02, StepLOD_03, StepLOD_04, StepLOD_05, EffectCreate, HitEffectKind, FourFoot

- 未发现命中 `TID` / `*ID` / `*TID` 的字段。

## ChatTable

- 文件：`data/tables/ChatTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：18
- 解析后的业务数据行数：14
- 字段总数：12
- 字段列表：TID, EngDesc, LocalDesc, Type, RGB, ChannelName, Normal, EngHotKey_01, LocalHotKey_01, EngHotKey_02, LocalHotKey_02, AvailChat

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 14 | 14 | 0 | 0 | 表内唯一（可疑似主键） |

## CommandTable

- 文件：`data/tables/CommandTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：119
- 解析后的业务数据行数：115
- 字段总数：13
- 字段列表：TID, Category, Type, UserAuth, LocalCommand, EngCommand, Desc, Arg_Num, Arg1, Arg2, Arg3, Arg4, InputEx

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 115 | 115 | 0 | 0 | 表内唯一（可疑似主键） |

## ContentsOptionTable

- 文件：`data/tables/ContentsOptionTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：15
- 解析后的业务数据行数：11
- 字段总数：45
- 字段列表：TID, mSvrNo, mOptionNo, mOptionNm, mOptionDesc, mOptionDesc0, mOptionValue0, mOptionDesc1, mOptionValue1, mOptionDesc2, mOptionValue2, mOptionDesc3, mOptionValue3, mOptionDesc4, mOptionValue4, mOptionDesc5, mOptionValue5, mOptionDesc6, mOptionValue6, mOptionDesc7, mOptionValue7, mOptionDesc8, mOptionValue8, mOptionDesc9, mOptionValue9, mOptionDesc10, mOptionValue10, mOptionDesc11, mOptionValue11, mOptionDesc12, mOptionValue12, mOptionDesc13, mOptionValue13, mOptionDesc14, mOptionValue14, mOptionDesc15, mOptionValue15, mOptionDesc16, mOptionValue16, mOptionDesc17, mOptionValue17, mOptionDesc18, mOptionValue18, mOptionDesc19, mOptionValue19

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 11 | 11 | 0 | 0 | 表内唯一（可疑似主键） |

## CustomizePreviewTable

- 文件：`data/tables/CustomizePreviewTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：12
- 解析后的业务数据行数：8
- 字段总数：30
- 字段列表：TID, Race, Gen, BaseEquip_Lance, BaseEquip_Staff, BaseEquip_Axe, BaseEquip_Bow, BaseEquip_Charkram, BaseEquip_Dagger, BaseEquip_Orb, BaseEquip_MagicGun, BaseEquip_Sword, BaseEquip_Wand, BaseEquip_Blade, BaseEquip_Arbalest, Movie_Lance, Movie_Staff, Movie_Axe, Movie_Bow, Movie_Charkram, Movie_Dagger, Movie_Orb, Movie_MagicGun, Movie_Sword, Movie_Wand, Movie_Blade, Movie_Arbalest, EquipView01, EquipView02, EquipView03

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 8 | 8 | 0 | 0 | 表内唯一（可疑似主键） |

## CustomizeTable

- 文件：`data/tables/CustomizeTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：3301
- 解析后的业务数据行数：3297
- 字段总数：16
- 字段列表：TID, Type, TermsTID, Name, EngName, Price, bCreate, Icon, Model, reqPCType, reqItem1, reqItemCount1, reqItem2, reqItemCount2, reqItem3, reqItemCount3

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 3297 | 3297 | 0 | 0 | 表内唯一（可疑似主键） |
| `TermsTID` | 88.54% | 2919 | 365 | 365 | 2554 | 明显重复（不能当主键） |

## EffectEventTable

- 文件：`data/tables/EffectEventTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：44
- 解析后的业务数据行数：40
- 字段总数：4
- 字段列表：ID, EventName, TargetEvent, ReturnEvent

- 未发现命中 `TID` / `*ID` / `*TID` 的字段。

## EntityTable

- 文件：`data/tables/EntityTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：760
- 解析后的业务数据行数：756
- 字段总数：34
- 字段列表：TID, Type, Kind, Property, Race, ShapeID, Color, Width, Height, Scale, Comment, EngTitle, EngName, LocalTitle, LocalName, UseIconType, WorldMapIcon, Level, Repeat, ItemDropTID, RegenR, RegenTimeMin, RegenTimeMax, Exp, ActionTID, Trigger, EntityState, EntityAni_01, EntityAni_02, EntityAni_03, QuestTID, QuestMissionTID, InsMapGroupTID, EventRange

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 756 | 756 | 0 | 0 | 表内唯一（可疑似主键） |
| `ShapeID` | 100.00% | 756 | 112 | 71 | 644 | 明显重复（不能当主键） |
| `ItemDropTID` | 100.00% | 756 | 536 | 1 | 220 | 明显重复（不能当主键） |
| `ActionTID` | 100.00% | 756 | 8 | 7 | 748 | 明显重复（不能当主键） |
| `QuestTID` | 100.00% | 756 | 471 | 13 | 285 | 明显重复（不能当主键） |
| `QuestMissionTID` | 100.00% | 756 | 484 | 3 | 272 | 明显重复（不能当主键） |
| `InsMapGroupTID` | 100.00% | 756 | 25 | 2 | 731 | 明显重复（不能当主键） |

## EventTable

- 文件：`data/tables/EventTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：29
- 解析后的业务数据行数：25
- 字段总数：25
- 字段列表：TID, SvrNo, Type, World, Fixed, Title, NoticeType, DayStart, DayEnd, DayWeek, TimeStart, TimeEnd, Exp, WExp, GhelldDrop, Fame, WarCoinCnt, MedalCnt, AddSkill, ItemDropRate, DropItem, GiftType, GiftTerm, GiftCheck, GiftMail

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 25 | 25 | 0 | 0 | 表内唯一（可疑似主键） |

## FamePointTable

- 文件：`data/tables/FamePointTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：24
- 解析后的业务数据行数：20
- 字段总数：7
- 字段列表：TID, EngAimName, EngDemolName, LocalAimName, LocalDemolName, ReqPoint, TotalPoint

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 20 | 20 | 0 | 0 | 表内唯一（可疑似主键） |

## FixedDummyAniTable

- 文件：`data/tables/FixedDummyAniTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：57
- 解析后的业务数据行数：53
- 字段总数：2
- 字段列表：TID, AniID

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 53 | 53 | 0 | 0 | 表内唯一（可疑似主键） |
| `AniID` | 100.00% | 53 | 53 | 0 | 0 | 表内唯一（可疑似主键） |

## GuildTable

- 文件：`data/tables/GuildTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：14
- 解析后的业务数据行数：10
- 字段总数：9
- 字段列表：TID, ReqPerson, ReqExp, ReqMoney, Tax, Slot, Name, Person, GuildSkill

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 10 | 10 | 0 | 0 | 表内唯一（可疑似主键） |

## HelpTable

- 文件：`data/tables/HelpTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：36
- 解析后的业务数据行数：32
- 字段总数：10
- 字段列表：TID, Comment, EngTitle, LocalTitle, EngName, LocalName, Type, Kind, EngDesc, LocalDesc

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 32 | 32 | 0 | 0 | 表内唯一（可疑似主键） |

## InstanceMapTable

- 文件：`data/tables/InstanceMapTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：121
- 解析后的业务数据行数：117
- 字段总数：29
- 字段列表：TID, GroupTID, Difficulty, Comment, EngName, LocalName, Goal, LimitTime, ReqJoinType, MinPerson, MaxPerson, ReqPerson, ReqMinLevel, ReqMaxLevel, ReqItem, ReqItem_Count, GoalPoint, GoalPoint_SSS_TID, GoalPoint_SS_TID, GoalPoint_S_TID, GoalPoint_A_TID, GoalPoint_B_TID, GoalPoint_F_TID, Img, Matching, ShowDifficulty, RolePerson, EngDesc, LocalDesc

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 117 | 117 | 0 | 0 | 表内唯一（可疑似主键） |
| `GroupTID` | 100.00% | 117 | 30 | 29 | 87 | 明显重复（不能当主键） |
| `GoalPoint_SSS_TID` | 100.00% | 117 | 82 | 1 | 35 | 明显重复（不能当主键） |
| `GoalPoint_SS_TID` | 100.00% | 117 | 82 | 1 | 35 | 明显重复（不能当主键） |
| `GoalPoint_S_TID` | 100.00% | 117 | 82 | 1 | 35 | 明显重复（不能当主键） |
| `GoalPoint_A_TID` | 100.00% | 117 | 82 | 1 | 35 | 明显重复（不能当主键） |
| `GoalPoint_B_TID` | 100.00% | 117 | 82 | 1 | 35 | 明显重复（不能当主键） |
| `GoalPoint_F_TID` | 100.00% | 117 | 81 | 1 | 36 | 明显重复（不能当主键） |

## InstanceRewardTable

- 文件：`data/tables/InstanceRewardTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：964
- 解析后的业务数据行数：960
- 字段总数：34
- 字段列表：TID, RewardTID, Comment, BoxColor, RewardItem01, RewardItemStack01, RewardRate01, RewardItem02, RewardItemStack02, RewardRate02, RewardItem03, RewardItemStack03, RewardRate03, RewardItem04, RewardItemStack04, RewardRate04, RewardItem05, RewardItemStack05, RewardRate05, RewardItem06, RewardItemStack06, RewardRate06, RewardItem07, RewardItemStack07, RewardRate07, RewardItem08, RewardItemStack08, RewardRate08, RewardItem09, RewardItemStack09, RewardRate09, RewardItem10, RewardItemStack10, RewardRate10

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 960 | 960 | 0 | 0 | 表内唯一（可疑似主键） |
| `RewardTID` | 100.00% | 960 | 80 | 80 | 880 | 明显重复（不能当主键） |

## InstanceRoundTable

- 文件：`data/tables/InstanceRoundTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：132
- 解析后的业务数据行数：128
- 字段总数：11
- 字段列表：TID, Comment, EngDesc, LocalDesc, Type, Round, RoundTime, RoundWaitTime, AutoRound, NpcTID, NpcCount

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 128 | 128 | 0 | 0 | 表内唯一（可疑似主键） |
| `NpcTID` | 100.00% | 128 | 98 | 1 | 30 | 明显重复（不能当主键） |

## Interpolator

- 文件：`data/tables/Interpolator.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：87
- 解析后的业务数据行数：83
- 字段总数：5
- 字段列表：ID, Content, Type, MaxTime, Data

- 未发现命中 `TID` / `*ID` / `*TID` 的字段。

## ItemAlchemyTable

- 文件：`data/tables/ItemAlchemyTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：22
- 解析后的业务数据行数：18
- 字段总数：35
- 字段列表：TID, Comment, CostGhelld, ItemTID, MaxMaterial, Item01TID, Item01Stack, Item01Rate, Item02TID, Item02Stack, Item02Rate, Item03TID, Item03Stack, Item03Rate, Item04TID, Item04Stack, Item04Rate, Item05TID, Item05Stack, Item05Rate, Item06TID, Item06Stack, Item06Rate, Item07TID, Item07Stack, Item07Rate, Item08TID, Item08Stack, Item08Rate, Item09TID, Item09Stack, Item09Rate, Item10TID, Item10Stack, Item10Rate

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 18 | 18 | 0 | 0 | 表内唯一（可疑似主键） |
| `ItemTID` | 100.00% | 18 | 18 | 0 | 0 | 表内唯一（可疑似主键） |
| `Item01TID` | 100.00% | 18 | 18 | 0 | 0 | 表内唯一（可疑似主键） |
| `Item02TID` | 100.00% | 18 | 18 | 0 | 0 | 表内唯一（可疑似主键） |
| `Item03TID` | 100.00% | 18 | 18 | 0 | 0 | 表内唯一（可疑似主键） |
| `Item04TID` | 100.00% | 18 | 18 | 0 | 0 | 表内唯一（可疑似主键） |
| `Item05TID` | 100.00% | 18 | 18 | 0 | 0 | 表内唯一（可疑似主键） |
| `Item06TID` | 100.00% | 18 | 13 | 1 | 5 | 明显重复（不能当主键） |
| `Item07TID` | 66.67% | 12 | 7 | 1 | 5 | 明显重复（不能当主键） |
| `Item08TID` | 100.00% | 18 | 2 | 2 | 16 | 明显重复（不能当主键） |
| `Item09TID` | 100.00% | 18 | 1 | 1 | 17 | 明显重复（不能当主键） |
| `Item10TID` | 100.00% | 18 | 1 | 1 | 17 | 明显重复（不能当主键） |

## ItemBoxTable

- 文件：`data/tables/ItemBoxTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：1290
- 解析后的业务数据行数：1286
- 字段总数：34
- 字段列表：TID, Comment, Group, GroupRate, BoxItem01, BoxItemStack01, DropRate01, BoxItem02, BoxItemStack02, DropRate02, BoxItem03, BoxItemStack03, DropRate03, BoxItem04, BoxItemStack04, DropRate04, BoxItem05, BoxItemStack05, DropRate05, BoxItem06, BoxItemStack06, DropRate06, BoxItem07, BoxItemStack07, DropRate07, BoxItem08, BoxItemStack08, DropRate08, BoxItem09, BoxItemStack09, DropRate09, BoxItem10, BoxItemStack10, DropRate10

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 1286 | 1286 | 0 | 0 | 表内唯一（可疑似主键） |

## ItemBreakTable

- 文件：`data/tables/ItemBreakTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：324
- 解析后的业务数据行数：320
- 字段总数：33
- 字段列表：TID, Comment, AddBreakNumber, AddBreakRate, BreakItem01, BreakItemStack01, BreakRate01, BreakItem02, BreakItemStack02, BreakRate02, BreakItem03, BreakItemStack03, BreakRate03, FGambleGhelld, FGambleItem01, FGambleItemStack01, FGambleRate01, FGambleItem02, FGambleItemStack02, FGambleRate02, FGambleItem03, FGambleItemStack03, FGambleRate03, SGambleGhelld, SGambleItem01, SGambleItemStack01, SGambleRate01, SGambleItem02, SGambleItemStack02, SGambleRate02, SGambleItem03, SGambleItemStack03, SGambleRate03

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 320 | 320 | 0 | 0 | 表内唯一（可疑似主键） |

## ItemCoinTable

- 文件：`data/tables/ItemCoinTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：12
- 解析后的业务数据行数：8
- 字段总数：52
- 字段列表：TID, Comment, EngName, LocalName, Type, Race, Coin, DropItem01, DropItemStack01, DropRate01, DropItem02, DropItemStack02, DropRate02, DropItem03, DropItemStack03, DropRate03, DropItem04, DropItemStack04, DropRate04, DropItem05, DropItemStack05, DropRate05, DropItem06, DropItemStack06, DropRate06, DropItem07, DropItemStack07, DropRate07, DropItem08, DropItemStack08, DropRate08, DropItem09, DropItemStack09, DropRate09, DropItem10, DropItemStack10, DropRate10, DropItem11, DropItemStack11, DropRate11, DropItem12, DropItemStack12, DropRate12, DropItem13, DropItemStack13, DropRate13, DropItem14, DropItemStack14, DropRate14, DropItem15, DropItemStack15, DropRate15

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 8 | 8 | 0 | 0 | 表内唯一（可疑似主键） |

## ItemDropLimitTable

- 文件：`data/tables/ItemDropLimitTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：5
- 解析后的业务数据行数：1
- 字段总数：5
- 字段列表：TID, Comment, Svr, ItemTID, ItemStack

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 1 | 1 | 0 | 0 | 表内唯一（可疑似主键） |
| `ItemTID` | 100.00% | 1 | 1 | 0 | 0 | 表内唯一（可疑似主键） |

## ItemDropTable

- 文件：`data/tables/ItemDropTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：8734
- 解析后的业务数据行数：8730
- 字段总数：53
- 字段列表：TID, Comment, GroupID, GroupRate, MinGhelld, MaxGhelld, AddDropNumber, AddDropRate, DropItem01, DropItemStack01, DropRate01, DropItem02, DropItemStack02, DropRate02, DropItem03, DropItemStack03, DropRate03, DropItem04, DropItemStack04, DropRate04, DropItem05, DropItemStack05, DropRate05, DropItem06, DropItemStack06, DropRate06, DropItem07, DropItemStack07, DropRate07, DropItem08, DropItemStack08, DropRate08, DropItem09, DropItemStack09, DropRate09, DropItem10, DropItemStack10, DropRate10, DropItem11, DropItemStack11, DropRate11, DropItem12, DropItemStack12, DropRate12, DropItem13, DropItemStack13, DropRate13, DropItem14, DropItemStack14, DropRate14, DropItem15, DropItemStack15, DropRate15

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 8730 | 8730 | 0 | 0 | 表内唯一（可疑似主键） |
| `GroupID` | 100.00% | 8730 | 1474 | 901 | 7256 | 明显重复（不能当主键） |

## ItemDropWorldTable

- 文件：`data/tables/ItemDropWorldTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：26
- 解析后的业务数据行数：22
- 字段总数：9
- 字段列表：TID, Desc, Svr, DropItemTID, DropItemStack, ItemRate, EventType, MinPLevel, MaxPLevel

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 22 | 22 | 0 | 0 | 表内唯一（可疑似主键） |
| `DropItemTID` | 100.00% | 22 | 22 | 0 | 0 | 表内唯一（可疑似主键） |

## ItemEnchantGlowTable

- 文件：`data/tables/ItemEnchantGlowTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：100
- 解析后的业务数据行数：96
- 字段总数：6
- 字段列表：TID, Comment, Grade, Step, Power, Color

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 96 | 96 | 0 | 0 | 表内唯一（可疑似主键） |

## ItemEnchantTable

- 文件：`data/tables/ItemEnchantTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：3683
- 解析后的业务数据行数：3679
- 字段总数：44
- 字段列表：TID, GroupTID, Step, Comment, SuccessRate, KeepRate, DownRate, ResetRate, CostGhelld, SourceItem01, Item01Value, SourceItem02, Item02Value, STR, CON, WIS, MEN, AGI, HPFixed, HPR, HPRBuff, MPFixed, MPR, MPRBuff, POPMin, POPMax, MOPMin, MOPMax, PD, MD, FD, WD, AD, LD, AP, DP, BP, CP, IGN_AT, PvP_AT, PvP_DF, AS, RS, CS

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 3679 | 3679 | 0 | 0 | 表内唯一（可疑似主键） |
| `GroupTID` | 100.00% | 3679 | 247 | 247 | 3432 | 明显重复（不能当主键） |

## ItemMatrixTable

- 文件：`data/tables/ItemMatrixTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：1020
- 解析后的业务数据行数：1016
- 字段总数：11
- 字段列表：WeaponName, CharName, HandType, TX, TY, TZ, RX, RY, RZ, Scale, CombatScale

- 未发现命中 `TID` / `*ID` / `*TID` 的字段。

## ItemMixTable

- 文件：`data/tables/ItemMixTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：67
- 解析后的业务数据行数：63
- 字段总数：19
- 字段列表：TID, Comment, SourceItem01, SourceItemCount01, MixRate01, MixItemResult01, MixItemCount01, MixRate02, MixItemResult02, MixItemCount02, MixRate03, MixItemResult03, MixItemCount03, MixRate04, MixItemResult04, MixItemCount04, MixRate05, MixItemResult05, MixItemCount05

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 63 | 63 | 0 | 0 | 表内唯一（可疑似主键） |

## ItemSeedTable

- 文件：`data/tables/ItemSeedTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：184
- 解析后的业务数据行数：180
- 字段总数：33
- 字段列表：TID, Comment, Group, CashRate, GhelldRate, Quality, STR, CON, WIS, MEN, AGI, HPFixed, HPR, HPRBuff, MPFixed, MPR, MPRBuff, POPMin, POPMax, MOPMin, MOPMax, PD, MD, AP, DP, BP, CP, IGN_AT, PvP_AT, PvP_DF, AS, RS, CS

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 180 | 180 | 0 | 0 | 表内唯一（可疑似主键） |

## ItemSetAbilityTable

- 文件：`data/tables/ItemSetAbilityTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：842
- 解析后的业务数据行数：838
- 字段总数：36
- 字段列表：TID, Comment, ReqTotal, STR, CON, WIS, MEN, AGI, HPFixed, HPR, HPRBuff, MPFixed, MPR, MPRBuff, POPMin, POPMax, MOPMin, MOPMax, PD, MD, FD, WD, AD, LD, AP, DP, BP, CP, IGN_AT, PvP_AT, PvP_DF, AS, RS, CS, EngDesc, LocalDesc

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 838 | 838 | 0 | 0 | 表内唯一（可疑似主键） |

## ItemSetTable

- 文件：`data/tables/ItemSetTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：354
- 解析后的业务数据行数：350
- 字段总数：4
- 字段列表：TID, Comment, ItemTID, SetAbilityTID

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 350 | 350 | 0 | 0 | 表内唯一（可疑似主键） |
| `ItemTID` | 100.00% | 350 | 350 | 0 | 0 | 表内唯一（可疑似主键） |
| `SetAbilityTID` | 100.00% | 350 | 182 | 144 | 168 | 明显重复（不能当主键） |

## ItemSocketTable

- 文件：`data/tables/ItemSocketTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：11
- 解析后的业务数据行数：7
- 字段总数：6
- 字段列表：TID, EquipCostGhelld, RemoveCostGhelld, SuccessRate, KeepRate, Comment

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 7 | 7 | 0 | 0 | 表内唯一（可疑似主键） |

## ItemTable

- 文件：`data/tables/ItemTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：25167
- 解析后的业务数据行数：25163
- 字段总数：104
- 字段列表：TID, Comment, EngName, LocalName, Type, Kind, Property, Level, Grade, Race, Gender, LimitLevel, LimitSTR, LimitCON, LimitWIS, LimitMEN, LimitAgility, LimitMainWeapon, LimitFamePointTID, ReqWeaponLevel, PenaltyRate, Area, PowerRangeMax, RelativeClass, STR, CON, WIS, MEN, AGI, HPFixed, HPR, HPRBuff, MPFixed, MPR, MPRBuff, POPMin, POPMax, MOPMin, MOPMax, PD, MD, FD, WD, AD, LD, AP, DP, BP, CP, IGN_AT, PvP_AT, PvP_DF, AS, RS, CS, SetTID, CoolTime, UseSkillTID, LearnSkillTID, SocketTID, Socket, CashSocket, RecipeTID, EnchantTID, EnchantStepMax, SeedOption, Cash, SpecialTID, SpecialValue, AlchemyValue, AlchemyTID, MixTID, BreakTID, BoxTID, QuestTID, SalePrice, PurchasePrice, SaleFamePoint, PurchaseFamePoint, ReqMedalKind, SaleMedal, PurchaseMedal, ItemRestrict, StackCount, MaxCount, Consume, BindType, UnBindCount, Stoppable, MaxDurability, MinDurability, Crash, DecreationDurability, Repairable, ItemMeshLeft, ItemMeshRight, ItemMeshScale, UseEffect, UseSound, TreeDeps_01, TreeDeps_02, ItemIcon, EngDesc, LocalDesc

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 25163 | 25163 | 0 | 0 | 表内唯一（可疑似主键） |
| `LimitFamePointTID` | 100.00% | 25163 | 3 | 1 | 25160 | 明显重复（不能当主键） |
| `SetTID` | 100.00% | 25163 | 365 | 365 | 24798 | 明显重复（不能当主键） |
| `UseSkillTID` | 100.00% | 25163 | 409 | 22 | 24754 | 明显重复（不能当主键） |
| `LearnSkillTID` | 100.00% | 25163 | 27 | 5 | 25136 | 明显重复（不能当主键） |
| `SocketTID` | 100.00% | 25163 | 8 | 8 | 25155 | 明显重复（不能当主键） |
| `RecipeTID` | 99.99% | 25161 | 3811 | 1 | 21350 | 明显重复（不能当主键） |
| `EnchantTID` | 100.00% | 25163 | 202 | 199 | 24961 | 明显重复（不能当主键） |
| `SpecialTID` | 99.99% | 25161 | 22 | 21 | 25139 | 明显重复（不能当主键） |
| `AlchemyTID` | 0.80% | 202 | 19 | 1 | 183 | 明显重复（不能当主键） |
| `MixTID` | 100.00% | 25163 | 64 | 1 | 25099 | 明显重复（不能当主键） |
| `BreakTID` | 100.00% | 25163 | 313 | 313 | 24850 | 明显重复（不能当主键） |
| `BoxTID` | 100.00% | 25163 | 303 | 1 | 24860 | 明显重复（不能当主键） |
| `QuestTID` | 100.00% | 25163 | 133 | 3 | 25030 | 明显重复（不能当主键） |

## LevelCompareTable

- 文件：`data/tables/LevelCompareTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：25
- 解析后的业务数据行数：21
- 字段总数：16
- 字段列表：TID, Compare, PC2PC_HitPoint, PC2NPC_HitPoint, NPC2PC_HitPoint, NPC2NPC_HitPoint, PC2PC_Attack, PC2NPC_Attack, NPC2PC_Attack, NPC2NPC_Attack, PC_WeaponExp, PC_Drop, PC_Exp, PC_Ghelld, PC_GatherExp, PC_GatherProba

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 21 | 21 | 0 | 0 | 表内唯一（可疑似主键） |

## LevelupTable

- 文件：`data/tables/LevelupTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：404
- 解析后的业务数据行数：400
- 字段总数：14
- 字段列表：TID, Race, Level, Exp, TotalExp, AcquisitionStatPoint, ResetStatPoint, HP, MP, HPRBuff, MPRBuff, DP, BP, AP

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 400 | 400 | 0 | 0 | 表内唯一（可疑似主键） |

## LocalizeTable

- 文件：`data/tables/LocalizeTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：24
- 解析后的业务数据行数：20
- 字段总数：4
- 字段列表：TID, Column, Pos, Desc

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 20 | 20 | 0 | 0 | 表内唯一（可疑似主键） |

## MailTable

- 文件：`data/tables/MailTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：53
- 解析后的业务数据行数：49
- 字段总数：14
- 字段列表：TID, Type, Kind, Value, ToRealm, Property, Title, Main, Sender, KeepTerm, AddGhelld, AddItemTID, AddItemCount, LocalDesc

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 49 | 49 | 0 | 0 | 表内唯一（可疑似主键） |
| `AddItemTID` | 87.76% | 43 | 19 | 4 | 24 | 明显重复（不能当主键） |

## MapTable

- 文件：`data/tables/MapTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：503
- 解析后的业务数据行数：499
- 字段总数：9
- 字段列表：TID, WorldTID, MapX, MapY, SectorCountX, SectorCountY, LevelName, Desc, Path

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 499 | 499 | 0 | 0 | 表内唯一（可疑似主键） |
| `WorldTID` | 100.00% | 499 | 167 | 6 | 332 | 明显重复（不能当主键） |

## MessageBoxTable

- 文件：`data/tables/MessageBoxTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：164
- 解析后的业务数据行数：160
- 字段总数：10
- 字段列表：TID, String, EngTitle, LocalTitle, EngContents, LocalContents, FontColor, FontSize, EngDesc, LocalDesc

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 160 | 160 | 0 | 0 | 表内唯一（可疑似主键） |

## MessageTable

- 文件：`data/tables/MessageTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：2042
- 解析后的业务数据行数：2038
- 字段总数：9
- 字段列表：TID, Position, String, EngContents, LocalContents, System_Voice, FontColor, FontSize, Comment

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 2038 | 2038 | 0 | 0 | 表内唯一（可疑似主键） |

## NaviPointTable

- 文件：`data/tables/NaviPointTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：27337
- 解析后的业务数据行数：27333
- 字段总数：4
- 字段列表：TID, WorldTID, Pos, Link

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 27333 | 27333 | 0 | 0 | 表内唯一（可疑似主键） |
| `WorldTID` | 100.00% | 27333 | 98 | 98 | 27235 | 明显重复（不能当主键） |

## NpcBrainTable

- 文件：`data/tables/NpcBrainTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：3211
- 解析后的业务数据行数：3207
- 字段总数：24
- 字段列表：TID, Comment, BaseGoal, DetectRadius, WanderRadius, BattleRadius, BattleRestore, AttackSkill, AttackRate, Action01, Action02, Action03, Action04, Action05, Action06, Action07, Action08, Action09, Action10, Talk_01, Talk_02, Talk_03, Talk_04, Talk_05

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 3207 | 3207 | 0 | 0 | 表内唯一（可疑似主键） |

## NpcDlgStringTable

- 文件：`data/tables/NpcDlgStringTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：728
- 解析后的业务数据行数：724
- 字段总数：10
- 字段列表：TID, Type, TypeCondition, MinLV, MaxLV, Race, EngContents, LocalContents, EngDesc, LocalDesc

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 724 | 724 | 0 | 0 | 表内唯一（可疑似主键） |

## NpcTable

- 文件：`data/tables/NpcTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：4707
- 解析后的业务数据行数：4703
- 字段总数：61
- 字段列表：TID, Type, Kind, Property, SpecialValue, Race, Grade, WeaponType, ShapeID, Comment, EngTitle, EngName, LocalTitle, LocalName, UseIconType, WorldMapIcon, Level, HP, MP, HPR, MPR, POPMin, POPMax, MOPMin, MOPMax, PD, MD, FD, WD, AD, LD, DP, BP, AP, CP, IGN_AT, AS, Ws, WsAni, RS, RsAni, CS, Exp, ItemDropTID, MapDropTID, SaleTID, Motion, EventRange, Color, Width, Height, Scale, NpcBrain, RegenR, RegenTimeMin, RegenTimeMax, Greeting, Eventlist, Gossip, GreetVoice, GoodbyeVoice

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 4703 | 4703 | 0 | 0 | 表内唯一（可疑似主键） |
| `ShapeID` | 100.00% | 4703 | 576 | 453 | 4127 | 明显重复（不能当主键） |
| `ItemDropTID` | 99.98% | 4702 | 246 | 215 | 4456 | 明显重复（不能当主键） |
| `MapDropTID` | 99.98% | 4702 | 21 | 21 | 4681 | 明显重复（不能当主键） |
| `SaleTID` | 100.00% | 4703 | 92 | 46 | 4611 | 明显重复（不能当主键） |

## PartyExpTable

- 文件：`data/tables/PartyExpTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：59
- 解析后的业务数据行数：55
- 字段总数：14
- 字段列表：TID, Level, Exp, SkillTID_01, SkillTID_02, SkillTID_03, SkillTID_04, SkillTID_05, SkillTID_06, SkillTID_07, SkillTID_08, SkillTID_09, SkillTID_10, InsMapTID

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 55 | 55 | 0 | 0 | 表内唯一（可疑似主键） |
| `InsMapTID` | 100.00% | 55 | 7 | 7 | 48 | 明显重复（不能当主键） |

## PcTable

- 文件：`data/tables/PcTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：45
- 解析后的业务数据行数：41
- 字段总数：44
- 字段列表：TID, Type, Kind, Race, Gen, MainWeapon, ShapeID, Comment, Level, STR, CON, WIS, MEN, AGI, HP, MP, HPR, MPR, HPRBuff, MPRBuff, POPMin, POPMax, MOPMin, MOPMax, PD, MD, FD, WD, AD, LD, DP, BP, AP, CP, IGN_AT, PvP_AT, PvP_DF, AS, RS, CS, Motion, Width, Height, Scale

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 41 | 41 | 0 | 0 | 表内唯一（可疑似主键） |
| `ShapeID` | 100.00% | 41 | 9 | 8 | 32 | 明显重复（不能当主键） |

## PortalTable

- 文件：`data/tables/PortalTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：244
- 解析后的业务数据行数：240
- 字段总数：17
- 字段列表：TID, Comment, EngName, LocalName, SrcEntityTID, DstEntityTID, DstWorldPlaceTID, Radius, reqRace, reqMinLV, reqMaxLV, reqQuest, reqMoney, reqItem, reqItemCount, reqHaveItem, reqHaveItemCount

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 240 | 240 | 0 | 0 | 表内唯一（可疑似主键） |
| `SrcEntityTID` | 100.00% | 240 | 52 | 52 | 188 | 明显重复（不能当主键） |
| `DstEntityTID` | 100.00% | 240 | 52 | 52 | 188 | 明显重复（不能当主键） |
| `DstWorldPlaceTID` | 100.00% | 240 | 52 | 52 | 188 | 明显重复（不能当主键） |

## ProductItemTable

- 文件：`data/tables/ProductItemTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：3814
- 解析后的业务数据行数：3810
- 字段总数：25
- 字段列表：TID, ProductType, ProductKind, Comment, ItemTID, ProductLevel, RecipeExp, CostGhelld, CompleteItemTID, SourceItem01, Value01, SourceItem02, Value02, SourceItem03, Value03, SourceItem04, Value04, SourceItem05, Value05, SourceItem06, Value06, SourceItem07, Value07, SourceItem08, Value08

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 3810 | 3810 | 0 | 0 | 表内唯一（可疑似主键） |
| `ItemTID` | 100.00% | 3810 | 3810 | 0 | 0 | 表内唯一（可疑似主键） |
| `CompleteItemTID` | 100.00% | 3810 | 3741 | 5 | 69 | 明显重复（不能当主键） |

## ProductLvTable

- 文件：`data/tables/ProductLvTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：444
- 解析后的业务数据行数：440
- 字段总数：6
- 字段列表：TID, ProductType, Lv, Exp, TotalExp, Comment

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 440 | 440 | 0 | 0 | 表内唯一（可疑似主键） |

## QuestCinemaTable

- 文件：`data/tables/QuestCinemaTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：195
- 解析后的业务数据行数：191
- 字段总数：6
- 字段列表：TID, Skip, LimitTime, BGM, SceneTID, Comment

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 191 | 191 | 0 | 0 | 表内唯一（可疑似主键） |
| `SceneTID` | 100.00% | 191 | 191 | 0 | 0 | 表内唯一（可疑似主键） |

## QuestDropTable

- 文件：`data/tables/QuestDropTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：799
- 解析后的业务数据行数：795
- 字段总数：8
- 字段列表：TID, Comment, QuestTID, NpcTID, ItemTID, DropRate, DropStack, DropAll

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 795 | 795 | 0 | 0 | 表内唯一（可疑似主键） |
| `QuestTID` | 100.00% | 795 | 655 | 120 | 140 | 明显重复（不能当主键） |
| `NpcTID` | 100.00% | 795 | 591 | 166 | 204 | 明显重复（不能当主键） |
| `ItemTID` | 100.00% | 795 | 639 | 118 | 156 | 明显重复（不能当主键） |

## QuestMissionTable

- 文件：`data/tables/QuestMissionTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：3821
- 解析后的业务数据行数：3817
- 字段总数：12
- 字段列表：TID, EngTitle, EngPurpose, LocalTitle, LocalPurpose, Type, Value, Value2, Count, RemoveItem, WorldTID, MapXYZ

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 3817 | 3817 | 0 | 0 | 表内唯一（可疑似主键） |
| `WorldTID` | 100.00% | 3817 | 65 | 56 | 3752 | 明显重复（不能当主键） |

## QuestRewardTable

- 文件：`data/tables/QuestRewardTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：5384
- 解析后的业务数据行数：5380
- 字段总数：5
- 字段列表：TID, Type, Value, Count, IsSelect

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 5380 | 5380 | 0 | 0 | 表内唯一（可疑似主键） |

## QuestSceneTable

- 文件：`data/tables/QuestSceneTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：573
- 解析后的业务数据行数：569
- 字段总数：16
- 字段列表：TID, Comment, Type, Movie, Image, Camera, TargetTID, EngDesc, LocalDesc, , , , , , , 

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 569 | 569 | 0 | 0 | 表内唯一（可疑似主键） |
| `TargetTID` | 100.00% | 569 | 65 | 63 | 504 | 明显重复（不能当主键） |

## QuestTable

- 文件：`data/tables/QuestTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：3280
- 解析后的业务数据行数：3276
- 字段总数：40
- 字段列表：TID, Type, EngTitle, EngMainScript, EngProgressScript, EngFinishScript, EngMiniBarFinish, LocalTitle, LocalMainScript, LocalProgressScript, LocalFinishScript, LocalMiniBarFinish, Area, Grade, Level, Repeat, RepeatDay, Share, StartType, StartValue, StartCinemaTID, FinishType, FinishValue, FinishCinemaTID, TimeOut, PrevQuest, NextQuest, DemandRace, DemandLowLv, DemandMaxLv, DemandWeapon, DemandWLv, GiveItem1, GiveItemCnt1, GiveItem2, GiveItemCnt2, EventTID, MissionTID, RewardTID, DropTID

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 3276 | 3276 | 0 | 0 | 表内唯一（可疑似主键） |
| `StartCinemaTID` | 100.00% | 3276 | 23 | 1 | 3253 | 明显重复（不能当主键） |
| `FinishCinemaTID` | 99.97% | 3275 | 1 | 1 | 3274 | 明显重复（不能当主键） |
| `EventTID` | 100.00% | 3276 | 1 | 1 | 3275 | 明显重复（不能当主键） |
| `MissionTID` | 100.00% | 3276 | 3276 | 0 | 0 | 表内唯一（可疑似主键） |
| `RewardTID` | 100.00% | 3276 | 2886 | 11 | 390 | 明显重复（不能当主键） |
| `DropTID` | 100.00% | 3276 | 542 | 2 | 2734 | 明显重复（不能当主键） |

## RandomNodeTable

- 文件：`data/tables/RandomNodeTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：95
- 解析后的业务数据行数：91
- 字段总数：2
- 字段列表：CharName, NodeName

- 未发现命中 `TID` / `*ID` / `*TID` 的字段。

## SaleTable

- 文件：`data/tables/SaleTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：4448
- 解析后的业务数据行数：4444
- 字段总数：13
- 字段列表：TID, Comment, SaleTID, slot, ItemTID, ItemMaxSale, ItemMaxBuy, SaleDay_01, SaleStart_01, SaleEnd_01, SaleDay_02, SaleStart_02, SaleEnd_02

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 4444 | 4444 | 0 | 0 | 表内唯一（可疑似主键） |
| `SaleTID` | 100.00% | 4444 | 117 | 117 | 4327 | 明显重复（不能当主键） |
| `ItemTID` | 100.00% | 4444 | 3635 | 497 | 809 | 明显重复（不能当主键） |

## ServerInfoTable

- 文件：`data/tables/ServerInfoTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：17
- 解析后的业务数据行数：13
- 字段总数：10
- 字段列表：TID, Comment, ServerName, StateFlag, LoginQueue, PCMax, NpcMax, EntityMax, SummonMax, ObjectMax

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 13 | 13 | 0 | 0 | 表内唯一（可疑似主键） |

## SkillBaseAttackTable

- 文件：`data/tables/SkillBaseAttackTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：14
- 解析后的业务数据行数：10
- 字段总数：4
- 字段列表：TID, WeaponKind, SkillTID, CriticalSkillTID

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 10 | 10 | 0 | 0 | 表内唯一（可疑似主键） |
| `SkillTID` | 100.00% | 10 | 10 | 0 | 0 | 表内唯一（可疑似主键） |
| `CriticalSkillTID` | 100.00% | 10 | 10 | 0 | 0 | 表内唯一（可疑似主键） |

## SkillComboTable

- 文件：`data/tables/SkillComboTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：40
- 解析后的业务数据行数：36
- 字段总数：16
- 字段列表：TID, ComboSkillGroup_0, ComboSkillGroup_1, ComboSkillGroup_2, ComboSkillGroup_3, ComboSkillGroup_4, MinComboSkillTime_0, MinComboSkillTime_1, MinComboSkillTime_2, MinComboSkillTime_3, MinComboSkillTime_4, MaxComboSkillTime_0, MaxComboSkillTime_1, MaxComboSkillTime_2, MaxComboSkillTime_3, MaxComboSkillTime_4

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 36 | 36 | 0 | 0 | 表内唯一（可疑似主键） |

## SkillLearnTable

- 文件：`data/tables/SkillLearnTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：364
- 解析后的业务数据行数：360
- 字段总数：7
- 字段列表：TID, Comment, WeaponType, SkillTID, DX2, DY2, NextTID

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 360 | 360 | 0 | 0 | 表内唯一（可疑似主键） |
| `SkillTID` | 100.00% | 360 | 360 | 0 | 0 | 表内唯一（可疑似主键） |
| `NextTID` | 0.00% | 0 | 0 | 0 | 0 | 空字段（不能当主键） |

## SkillTable

- 文件：`data/tables/SkillTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：11330
- 解析后的业务数据行数：11326
- 字段总数：70
- 字段列表：TID, SkillGroup, SkillLevel, Comment, EngName, LocalName, LearnType, Type, Kind, Property, BuffPosition, BuffDelete, InputType, Target, MaxArea_01, MaxArea_02, VolumeArea, MinRange, MaxRange, AutoLearnSkillTID, ComboSkillGroup, ReqHP, ReqMP, NumericalClass, KindValue, SuccessRate, AddDamage, AgroValue, AffectType, AffectDuration, AffectCount, CoolTime, GlobalCoolTime, NextSkillTID, AddtionSkillTID, AddtionRate, ReqItemTID, ReqItemTIDCount, CastMoveAbility, CastingAniID, UpCastingAniID, CastingTime, CastingFailRate, CastingDelayTime, CastingDelayRate, Race, LimitWeapon, LimitMainWeapon, LimitWeaponLevel, OpenPoint, LimitCharLevel, LearnSkillPoint, PreConditionTID_01, PreConditionTID_02, SkillArea, NowGrade, MaxGrade, AniID, AniTime, UpAniID, UpAniTime, EnableMoving, EffectiveRange, AutoAttack, ActionEffectname, CameraID, SkillIconID, EngDesc, LocalDesc, AlarmMsg

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 11326 | 11326 | 0 | 0 | 表内唯一（可疑似主键） |
| `AutoLearnSkillTID` | 100.00% | 11326 | 11 | 1 | 11315 | 明显重复（不能当主键） |
| `NextSkillTID` | 100.00% | 11326 | 36 | 1 | 11290 | 明显重复（不能当主键） |
| `AddtionSkillTID` | 100.00% | 11326 | 1263 | 11 | 10063 | 明显重复（不能当主键） |
| `ReqItemTID` | 100.00% | 11326 | 5 | 1 | 11321 | 明显重复（不能当主键） |
| `CastingAniID` | 100.00% | 11326 | 20 | 18 | 11306 | 明显重复（不能当主键） |
| `UpCastingAniID` | 100.00% | 11326 | 1 | 1 | 11325 | 明显重复（不能当主键） |
| `AniID` | 100.00% | 11326 | 223 | 199 | 11103 | 明显重复（不能当主键） |
| `UpAniID` | 100.00% | 11326 | 89 | 69 | 11237 | 明显重复（不能当主键） |
| `CameraID` | 100.00% | 11326 | 1 | 1 | 11325 | 明显重复（不能当主键） |
| `SkillIconID` | 100.00% | 11326 | 503 | 437 | 10823 | 明显重复（不能当主键） |

## StatTable

- 文件：`data/tables/StatTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：2008
- 解析后的业务数据行数：2004
- 字段总数：14
- 字段列表：TID, StatClass, StatPoint, StrPOPMin, StrPOPMax, ConMaxHp, ConHPR, WisMOPMin, WisMOPMax, MenMaxMp, MenMPR, AgilityDP, AgilityAP, AgilityCP

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 2004 | 2004 | 0 | 0 | 表内唯一（可疑似主键） |

## SummonTable

- 文件：`data/tables/SummonTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：432
- 解析后的业务数据行数：428
- 字段总数：9
- 字段列表：TID, Comment, NPCTID, AiTID, GoalTID, Time, AreaTID, AS, RS

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 428 | 428 | 0 | 0 | 表内唯一（可疑似主键） |
| `NPCTID` | 100.00% | 428 | 426 | 2 | 2 | 高唯一但非严格唯一 |
| `AiTID` | 0.00% | 0 | 0 | 0 | 0 | 空字段（不能当主键） |
| `GoalTID` | 0.00% | 0 | 0 | 0 | 0 | 空字段（不能当主键） |
| `AreaTID` | 98.36% | 421 | 1 | 1 | 420 | 明显重复（不能当主键） |

## TerrainSurfaceTable

- 文件：`data/tables/TerrainSurfaceTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：189
- 解析后的业务数据行数：185
- 字段总数：11
- 字段列表：TID, Name, FootSound_L, FootSound_R, FootSound_Up, FootSound_Down, FootEffect_L, FootEffect_R, FootEffect_Up, FootEffect_Down, Desc

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 185 | 185 | 0 | 0 | 表内唯一（可疑似主键） |

## TipTable

- 文件：`data/tables/TipTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：106
- 解析后的业务数据行数：102
- 字段总数：4
- 字段列表：TID, Type, EngDesc, LocalDesc

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 102 | 102 | 0 | 0 | 表内唯一（可疑似主键） |

## TitleTable

- 文件：`data/tables/TitleTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：7
- 解析后的业务数据行数：3
- 字段总数：4
- 字段列表：TID, EngName, LocalName, FinishCount

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 3 | 3 | 0 | 0 | 表内唯一（可疑似主键） |

## ToolWeaponTable

- 文件：`data/tables/ToolWeaponTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：17
- 解析后的业务数据行数：13
- 字段总数：4
- 字段列表：TID, Name, LeftMesh, RightMesh

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 13 | 13 | 0 | 0 | 表内唯一（可疑似主键） |

## TriggerTable

- 文件：`data/tables/TriggerTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：348
- 解析后的业务数据行数：344
- 字段总数：12
- 字段列表：TID, Comment, Owner, Trigger, Target, Action, ConUnion, ConLevel, ConQuest, Loop, TriggerMessageTarget, TriggerMessage

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 344 | 344 | 0 | 0 | 表内唯一（可疑似主键） |

## TutorialTable

- 文件：`data/tables/TutorialTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：70
- 解析后的业务数据行数：66
- 字段总数：12
- 字段列表：TID, Comment, Type, Value, TitleMsg, TutorialMovie, ExplainMsg, ToolTip, UIP, ParentControl, ChildControl, Offset

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 66 | 66 | 0 | 0 | 表内唯一（可疑似主键） |

## WarContentsTable

- 文件：`data/tables/WarContentsTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：27
- 解析后的业务数据行数：23
- 字段总数：40
- 字段列表：TID, Comment, EngName, LocalName, Type, Kind, Goal, MaxPerson, ReqMinLevel, ReqMaxLevel, ReqItem, ReqItemCount, OptionValue1, OptionValue2, OptionValue3, OptionValue4, OptionValue5, StandbyTime, LimitTime, MapTID, StartDay, StartTime, FameKill, MinContribution, Contribution, RankFame, GoalAchieve, FameWinPoint, FameLosePoint, FameDrawPoint, CampBuff, WinCoin, LoseCoin, DrawCoin, WinMail, LoseMail, DrawMail, EngDesc, LocalDesc, WarImg

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 23 | 23 | 0 | 0 | 表内唯一（可疑似主键） |
| `MapTID` | 100.00% | 23 | 23 | 0 | 0 | 表内唯一（可疑似主键） |

## WarUniformTable

- 文件：`data/tables/WarUniformTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：8
- 解析后的业务数据行数：4
- 字段总数：3
- 字段列表：TID, Comment, UniformItemID

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 4 | 4 | 0 | 0 | 表内唯一（可疑似主键） |
| `UniformItemID` | 100.00% | 4 | 2 | 2 | 2 | 明显重复（不能当主键） |

## WeaponAbilityTable

- 文件：`data/tables/WeaponAbilityTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：24
- 解析后的业务数据行数：20
- 字段总数：10
- 字段列表：TID, Group, Lv, POPMin, POPMax, MOPMin, MOPMax, AP, CP, AS

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 20 | 20 | 0 | 0 | 表内唯一（可疑似主键） |

## WeaponLvTable

- 文件：`data/tables/WeaponLvTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：1007
- 解析后的业务数据行数：1003
- 字段总数：27
- 字段列表：TID, Kind, Lv, Exp, TotalExp, MainSp, ResetMainSp, SubSp, ResetSubSp, Comment, Ghelld, HPRBuff, MPRBuff, POPMin, POPMax, MOPMin, MOPMax, IGN_AT, AP, CP, BP, AS, STR, CON, WIS, MEN, AGI

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 1003 | 1003 | 0 | 0 | 表内唯一（可疑似主键） |

## WeatherTable

- 文件：`data/tables/WeatherTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：132
- 解析后的业务数据行数：128
- 字段总数：4
- 字段列表：TID, Type, Name, Attrib

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 128 | 128 | 0 | 0 | 表内唯一（可疑似主键） |

## WorldEnvLightTable

- 文件：`data/tables/WorldEnvLightTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：8978
- 解析后的业务数据行数：8974
- 字段总数：13
- 字段列表：TID, WorldTID, Type, Name, Pos, Rotation, Ambient, Diffuse, Specular, Dimmer, Radius, SpotIn, SpotOut

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 8974 | 8974 | 0 | 0 | 表内唯一（可疑似主键） |
| `WorldTID` | 100.00% | 8974 | 70 | 69 | 8904 | 明显重复（不能当主键） |

## WorldEnvSoundTable

- 文件：`data/tables/WorldEnvSoundTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：5199
- 解析后的业务数据行数：5195
- 字段总数：8
- 字段列表：TID, WorldTID, Name, Pos, Min, Max, Volume, 

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 5195 | 5195 | 0 | 0 | 表内唯一（可疑似主键） |
| `WorldTID` | 100.00% | 5195 | 65 | 64 | 5130 | 明显重复（不能当主键） |

## WorldEnvWaterTable

- 文件：`data/tables/WorldEnvWaterTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：37
- 解析后的业务数据行数：33
- 字段总数：4
- 字段列表：TID, Name, ShaderName, ShaderAttrib

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 33 | 33 | 0 | 0 | 表内唯一（可疑似主键） |

## WorldMapUITable

- 文件：`data/tables/WorldMapUITable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：161
- 解析后的业务数据行数：157
- 字段总数：27
- 字段列表：TID, Comment, EngName, LocalName, Type, WorldTID, ParentTID, Map, LoadingMap, TipTID, RoadMap, StartX, StartY, EndX, EndY, C1StartX, C1StartY, C1EndX, C1EndY, C2StartX, C2StartY, C2EndX, C2EndY, C3StartX, C3StartY, C3EndX, C3EndY

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 157 | 157 | 0 | 0 | 表内唯一（可疑似主键） |
| `WorldTID` | 100.00% | 157 | 142 | 1 | 15 | 明显重复（不能当主键） |
| `ParentTID` | 100.00% | 157 | 4 | 4 | 153 | 明显重复（不能当主键） |
| `TipTID` | 59.24% | 93 | 15 | 10 | 78 | 明显重复（不能当主键） |

## WorldPlaceTable

- 文件：`data/tables/WorldPlaceTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：32300
- 解析后的业务数据行数：32296
- 字段总数：11
- 字段列表：TID, WorldTID, PlaceType, PlaceTypeTID, Pos, Rotation, Radius, GroupNpc, State, WarView, PatrolPos

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 32296 | 32296 | 0 | 0 | 表内唯一（可疑似主键） |
| `WorldTID` | 100.00% | 32296 | 118 | 117 | 32178 | 明显重复（不能当主键） |
| `PlaceTypeTID` | 100.00% | 32296 | 4375 | 2255 | 27921 | 明显重复（不能当主键） |

## WorldTable

- 文件：`data/tables/WorldTable.csv`
- Header 行：第 1 行
- 有效数据起始行：第 5 行
- 文件总行数：169
- 解析后的业务数据行数：165
- 字段总数：35
- 字段列表：TID, Type, LoadType, ContentsLimit, Name, EngName, Channel, MapX, MapY, MapSizeX, MapSizeY, WorldProperty, RebirthTime, Human_Pos, Human_Pos1, Human_Pos2, Human_Invasion, Human_Radius, MoonElf_Pos, MoonElf_Pos1, MoonElf_Pos2, MoonElf_Invasion, MoonElf_Radius, DragonScion_Pos, DragonScion_Pos1, DragonScion_Pos2, DragonScion_Invasion, DragonScion_Radius, Orc_Pos, Orc_Pos1, Orc_Pos2, Orc_Invasion, Orc_Radius, SunFilePath, Desc

| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TID` | 100.00% | 165 | 165 | 0 | 0 | 表内唯一（可疑似主键） |
