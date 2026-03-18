# operator_query_regression_samples

## 目的

本文把当前 Item / NPC / Quest / unified backend 的**真实数据代表样本**固化成可复用回归池，供未来 PR 在开发、自测、评审描述中重复使用。

这套样本只验证：

- 主域判定是否稳定
- 白名单路径是否仍被保守使用
- 歧义/未命中行为是否稳定
- 关键 TID、名称、直接关系与 pending_confirmation 约束是否稳定

这套样本**不用于**：

- 全量表扫描式产品行为
- UI 文案快照
- same-name TID 自动联想
- 低置信关系推断
- 白名单边界扩张

## 当前基线与已检查表

当前仓库已落地并纳入默认运营查询空间的主域边界：

- Item: `ItemTable.csv`
- NPC: `NpcTable.csv`
- Quest: `QuestTable.csv`
- supporting tables: `ItemSetTable.csv`、`ItemSetAbilityTable.csv`、`SaleTable.csv`、`ItemDropTable.csv`、`QuestMissionTable.csv`、`QuestRewardTable.csv`、`QuestDropTable.csv`

本次样本选择基于当前仓库 checked-in 真实数据，并按现有实现白名单边界验证，不新增任何域和关系推断。

> 说明：当前仓库中没有本地 `main` 分支引用可直接读取；本次以当前 work 分支上已合入的 Item / NPC / Quest / unified-backend 基线代码与 checked-in 表数据作为对照基线。

## 样本池

### Item 样本

| 样本 | 查询 / TID | 代表性 | 验证的白名单路径 / 规则 | 必须稳定的行为 |
| --- | --- | --- | --- | --- |
| exact item TID + numeric collision guard | `80` | 真实纯数字 TID，同时存在 NPC 80 / Item 80，适合验证 item 域显式查询不受跨域碰撞影响。 | `ItemTable.TID` 精确命中；不因 NPC 同号而自动改写 item 结果。 | `query_item("80")` 仍返回唯一 Item 80。 |
| exact item name | `声望销售` | 真实唯一物品名，且后续还能复用为 NPC shop 反向样本。 | `ItemTable.LocalName` 精确命中。 | 返回唯一 Item 20。 |
| equipment / set-chain | `100010`（魔术师头盔） | 真实套装成员，覆盖 set chain。 | `ItemTable.SetTID -> ItemSetTable -> ItemSetAbilityTable`。 | 返回唯一 Item 100010，且保留 set / set ability 记录。 |
| duplicate-name ambiguity | `盾牌` | 真实重名物品。 | `ItemTable.LocalName` 多候选保守返回。 | 保持 `matched_items=[]` 且 `candidates>=2`。 |

### NPC 样本

| 样本 | 查询 / TID | 代表性 | 验证的白名单路径 / 规则 | 必须稳定的行为 |
| --- | --- | --- | --- | --- |
| NPC with shop relations | `声望商店` | 真实 NPC 商店入口。 | `NpcTable.SaleTID -> SaleTable.SaleTID -> SaleTable.ItemTID -> ItemTable.TID`。 | 返回 `query_kind=npc`，shop section 至少保留 1 条直接商品关系。 |
| NPC with drop relations | `哥布林池塘抢夺者` | 真实唯一名掉落 NPC，避免同名 NPC 干扰。 | `NpcTable.ItemDropTID -> ItemDropTable.TID -> DropItemNN -> ItemTable.TID`。 | 返回 `query_kind=npc`，drop section 至少保留 1 条直接掉落关系。 |
| reverse lookup through shop | `声望销售` | 从 Item 反查 NPC shop 来源。 | item 反向走 `SaleTable` 白名单路径。 | 返回 `query_kind=item`，且至少回指 1 个 NPC shop 来源。 |
| numeric NPC-vs-Item ambiguity | `80` | 真实纯数字双命中。 | 纯数字同时命中 NPC / Item 时必须 ambiguous。 | 返回 `query_kind=ambiguous` 且 `sections=[]`。 |

### Quest 样本

| 样本 | 查询 / TID | 代表性 | 验证的白名单路径 / 规则 | 必须稳定的行为 |
| --- | --- | --- | --- | --- |
| exact quest name + quest-drop | `哥布林的异常繁殖` | 真实任务名，同时包含 confirmed quest drop。 | `QuestTable` 精确命中 + `QuestDropTable.QuestTID` 主事实来源。 | 返回 Quest 1，且 quest_drops 保持 confirmed。 |
| give-item path | `4`（持续不断地实验） | 真实任务 TID，包含 GiveItem1。 | `QuestTable.GiveItem1 -> ItemTable.TID`。 | GiveItem1 稳定解析为 `20173 / 雷诺亚粉末 / confirmed`。 |
| reward path + vector mission | `5`（秘密的托付） | 同时包含向量 `MissionTID`、向量 `RewardTID`、confirmed reward item、quest drop。 | 仅 `Type=1` reward 解析 Item；mission/reward 向量按顺序保守展开。 | 保留两个 mission、至少一个 confirmed reward item、至少一个 confirmed quest drop。 |
| prev quest vector handling | `926`（收藏家的梦想之用） | 真实 `PrevQuest` 向量字段。 | `PrevQuest` 向量字段仅保守暴露首个链接，并标记 `pending_confirmation`。 | `prev_quest.status` 保持 `pending_confirmation`，并输出向量 note。 |

### Unified backend 样本

| 样本 | 查询 | 代表性 | 验证的白名单路径 / 规则 | 必须稳定的行为 |
| --- | --- | --- | --- | --- |
| no-hint exact item lookup | `声望销售` | 真实 item-only 命中。 | 无 hint 时只落到 item 域。 | `domain=item, status=exact_match`。 |
| no-hint exact NPC lookup | `声望商店` | 真实 npc-only 命中。 | 无 hint 时只落到 npc 域。 | `domain=npc, status=exact_match`。 |
| no-hint exact quest lookup | `哥布林的异常繁殖` | 真实 quest-only 命中。 | 无 hint 时只落到 quest 域。 | `domain=quest, status=exact_match`。 |
| cross-domain ambiguity | `哥布林的宝物` | 真实 item / quest 同名碰撞。 | 跨主域同名时不自动选边。 | `domain=None, status=ambiguous`。 |
| numeric ambiguity | `80` | 真实 NPC / Item 数字碰撞。 | 保留 numeric ambiguity note。 | `domain=None, status=ambiguous`。 |
| not_found | `MISSING_OPERATOR_SAMPLE` | 稳定的仓库外查询字符串。 | 所有白名单主域未命中。 | `domain=None, status=not_found`。 |
| explicit domain_hint behavior | `哥布林的宝物` + `domain_hint=item|quest` | 同一歧义查询在显式 hint 下应稳定定向。 | `domain_hint` 优先于自动路由。 | `item` hint 命中 Item 20025；`quest` hint 命中 Quest 7。 |
| invalid domain_hint | `哥布林的宝物` + `domain_hint=world` | 统一路由曾显式修复的错误输入场景，需要纳入长期回归。 | 非法 `domain_hint` 必须显式报错，不能静默改路由。 | 返回 `domain=None, status=ambiguous`，且 `primary_payload=None`。 |

## 开发 / 测试工作流

### 哪些样本必须始终运行

未来涉及以下任一改动时，必须至少运行本回归套件：

- Item 查询命中逻辑、重名逻辑、set chain 逻辑
- NPC 商店 / 掉落 / item 反向来源逻辑
- Quest give-item / reward / quest-drop / prev-next / vector handling 逻辑
- unified backend 的自动路由、歧义、not_found、domain_hint 逻辑

推荐命令：

```bash
python -m unittest bwqy-v1/tests/test_operator_query_regression_samples.py
python -m unittest discover -s bwqy-v1/tests
```

### 未来如何新增或更新样本

1. 优先从**真实 checked-in 数据**中选样本。
2. 只新增能够代表某个白名单路径或保守规则的样本。
3. 修改 `tests/operator_query_regression_samples.py` 中的样本元数据。
4. 同步更新本文档中的样本表格与“必须稳定的行为”。
5. 如果样本变化来自数据更新或产品边界调整，PR 描述中必须说明：
   - 为什么旧样本不再适合
   - 新样本验证了什么规则
   - 哪些不变量保持不变

### PR 描述应如何引用这套样本

涉及查询逻辑的 PR 描述至少应写明：

- 受影响域：Item / NPC / Quest / Unified 中哪些域
- 本次覆盖了哪些 regression sample keys
- 这些样本是否只是“继续通过”，还是因为产品边界变化而被替换
- 若涉及 unified router，也应说明是否覆盖了 invalid domain_hint 样本
- 若替换样本，替换理由与保持不变的约束
