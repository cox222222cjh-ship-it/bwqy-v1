# Design: build-quest-query-v1

## Overview

Quest v1 的目标不是“任务百科”，而是围绕 Quest 主实体提供**最小但可闭环的运营查询能力**。

默认支持的 operator-facing questions：

- 这个任务的 mission objectives 是什么？
- 这个任务有哪些 reward entries？
- 这个任务是否绑定 quest-specific drop？
- 这个任务直接发哪些 item？
- 这个任务的前置和后续任务是谁？

Quest v1 只允许从 `QuestTable` 进入，再通过白名单关系表补充详情。

---

## Design goals

1. **Quest-first**：默认入口必须是 `QuestTable`，不是 relation table。
2. **Operator-oriented**：只回答运营高频、可解释的问题，不做泛化浏览。
3. **High-confidence only**：只输出高置信链路；不确定项必须标记“待确认”。
4. **Closed loop**：命中一个 Quest 后，可以在同一次响应中给出 mission / reward / quest drop / give item / prev-next 的最小闭环。
5. **Default-exclusion preserving**：默认排除表仍然保持排除，不因 Quest 域扩展而松动。

---

## Allowed query scope

### 1. Top-level searchable table whitelist

Quest v1 仅允许以下顶层入口：

- `QuestTable.csv`

可用搜索字段：

- `QuestTable.TID`
- `QuestTable.LocalName`
- 如实现阶段确认存在稳定英文名字段，可作为辅助字段；否则不默认纳入。

### 2. Supporting relation table whitelist

仅允许以下 Quest supporting relation tables：

- `QuestMissionTable.csv`
- `QuestRewardTable.csv`
- `QuestDropTable.csv`

仅为解释结果而允许读取、但**不升级为 Quest 主入口**的受控补充表：

- `ItemTable.csv`
  - 用于解释 `GiveItem1` / `GiveItem2`，以及 reward / quest drop 中可被高置信识别为 item 的引用。
- `NpcTable.csv`
  - 用于解释 `QuestDropTable.NpcTID` 对应的 NPC。

### 3. Relation whitelist

Quest v1 只允许以下高置信关系：

1. **Quest -> Mission**
   - `QuestTable.MissionTID -> QuestMissionTable.TID`

2. **Quest -> Reward**
   - `QuestTable.RewardTID -> QuestRewardTable.TID`
   - 允许同一 `RewardTID` 对应多行 reward entries。

3. **Quest -> QuestDrop**
   - 高置信主链：`QuestDropTable.QuestTID = QuestTable.TID`
   - `QuestTable.DropTID -> QuestDropTable.TID` 仅可作为补充校验线索；若未证实稳定一一对应，不得单独作为唯一事实来源。

4. **Quest -> GiveItem**
   - `QuestTable.GiveItem1 -> ItemTable.TID`
   - `QuestTable.GiveItem2 -> ItemTable.TID`

5. **Quest -> Prev/Next**
   - `QuestTable.PrevQuest -> QuestTable.TID`
   - `QuestTable.NextQuest -> QuestTable.TID`

### 4. Default exclusions

Quest v1 默认排除以下内容：

- 帮助 / 教学 / 文本类：`HelpTable`、`TutorialTable`、`TipTable`、`BanWordTable`、`Message*`。
- 角色表现 / 外观 / 引擎支持：所有 `Char*`、`Customize*`、`Effect*`、`Interpolator` 等。
- Quest 表现型支撑：`QuestCinemaTable`、`QuestSceneTable`。
- 默认导航上下文表：`WorldTable`、`MapTable`、`AreaTable`、`PortalTable`、`WorldPlaceTable`。
- 后续扩展域：`EventTable`、`Instance*`。
- 任何仅因字段名称看起来可连接、但尚未确认业务语义的表。

---

## Query strategy

### Entry behavior

- 输入先只在 `QuestTable` 上解析。
- 纯数字输入按 `QuestTable.TID` 精确匹配。
- 非纯数字输入按 quest 名称字段匹配。
- Quest v1 不因为同一输入也可能命中 item / NPC，就自动跨域切换；跨域检索应由上层多域路由单独定义。

### Resolution behavior

命中单个 Quest 后，系统按固定顺序解析：

1. quest 基础身份
2. prev / next
3. give items
4. missions
5. rewards
6. quest-specific drops

这样可保证结果按“主记录 -> 邻接关系”稳定展开，而不是按全仓表扫描拼装。

### No full-table-scan strategy

禁止把“遍历所有表寻找可能出现 quest id 的列”作为产品策略。

允许的实现方式应是：

- 明确白名单表；
- 明确白名单字段；
- 对 whitelist relation 预建索引或定向读取；
- 只在白名单关系上解析详情。

---

## Response shape

建议 Quest v1 使用稳定、可程序消费的响应结构：

```json
{
  "query": "xxx",
  "domain": "quest",
  "status": "ok | ambiguous | not_found | error",
  "quest": {
    "tid": 123,
    "name": "..."
  },
  "relations": {
    "prev_quest": { "tid": 0, "name": "...", "status": "confirmed | pending_confirmation | missing" },
    "next_quest": { "tid": 0, "name": "...", "status": "confirmed | pending_confirmation | missing" },
    "give_items": [
      { "slot": "GiveItem1", "item_tid": 0, "item_name": "...", "status": "confirmed | missing" }
    ],
    "missions": [
      { "mission_tid": 0, "fields": {}, "status": "confirmed" }
    ],
    "rewards": [
      { "reward_tid": 0, "type": "...", "value": 0, "resolved_item": null, "status": "confirmed | pending_confirmation" }
    ],
    "quest_drops": [
      {
        "quest_tid": 0,
        "npc_tid": 0,
        "npc_name": "...",
        "item_tid": 0,
        "item_name": "...",
        "status": "confirmed | pending_confirmation"
      }
    ]
  },
  "notes": []
}
```

设计约束：

- `quest` 必须始终是主锚点。
- 每类 relation 分区输出，不混成平铺表。
- 每条 relation 必须带状态位，便于区分 confirmed / missing / pending_confirmation。
- 对 `QuestRewardTable.Value` 这类受 `Type` 影响的字段，若无法高置信解析成 item / currency / other typed reward，应保留原始值并标记解释状态。

---

## Ambiguity handling

### 1. Quest 主记录歧义

- 若名称查询命中多个 Quest，返回 `ambiguous`，列出候选 quest 列表。
- 不得默认猜测第一条。

### 2. Missing relation target

- 若 `PrevQuest` / `NextQuest` / `GiveItem1` / `GiveItem2` 指向空值、0 或无效引用，返回 `missing`，而不是伪造关系。

### 3. Reward interpretation ambiguity

- 若 `QuestRewardTable.Type` 可以解释奖励类型，但 `Value` 的业务含义仍不充分，则只输出“reward entry exists”，并将详细解释标记为 `pending_confirmation`。
- 不得仅因 `Value` 是数字就自动映射到 `ItemTable.TID`。

### 4. QuestDrop ambiguity

- `QuestDropTable.QuestTID = QuestTable.TID` 可作为主事实来源。
- 如果实现阶段发现 `QuestTable.DropTID` 与 `QuestDropTable.TID` 并非稳定一致，则 `DropTID` 只能作为补充诊断信息，不得主导结果。

### 5. Same-name TID prohibition

- 除本设计中显式列出的白名单字段外，不得因为任意列也叫 `TID` 就自动联表。

---

## Risks and mitigations

1. **QuestReward 解释过度**
   - 风险：把 `Value` 误解释成 item / currency / points。
   - 缓解：先按 entry 展示，并对类型解释做状态标记。

2. **QuestDrop 双链路不一致**
   - 风险：`DropTID` 与 `QuestTID` 关系并不稳定。
   - 缓解：以 `QuestDropTable.QuestTID` 为主；`DropTID` 只做辅助校验。

3. **Quest 名称重复**
   - 风险：名称查询多命中。
   - 缓解：显式返回候选列表，要求用户二次确认。

4. **范围滑坡**
   - 风险：实现时顺手把 map / event / scene / cinema 拉进默认结果。
   - 缓解：在 OpenSpec 中写死 whitelist 与 exclusions，并在测试中加负例。
