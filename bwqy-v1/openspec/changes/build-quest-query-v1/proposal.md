# Change Proposal: build-quest-query-v1

## Summary

新增一个独立的 OpenSpec change：`build-quest-query-v1`。

本次 change 仅定义 **Quest v1 的最小运营查询闭环**，用于回答运营高频且高置信的问题：

- 这个任务的目标组是什么？
- 这个任务发什么奖励？
- 这个任务是否绑定任务专属掉落？
- 这个任务会直接发哪些物品？
- 这个任务的前置 / 后续任务是什么？

Quest v1 仍坚持“运营对象白名单 + 高置信关系白名单”原则，不做通用任务百科，也不做全表浏览器。

## Why

当前仓库已经明确了默认运营查询空间的边界：

- `ItemTable`、`NpcTable`、`QuestTable` 是 primary operator entry points。
- Quest 适合作为独立对象域进入默认查询空间，但应围绕运营真实问题构建，而不是退回到 full-table scanning。
- 现有 item / NPC 最小能力都已经通过独立 change 收口，因此 Quest 应作为**新的 change**推进，而不是继续向旧 change 叠加范围。

## Goals

1. 定义 Quest v1 的默认表白名单与默认排除策略。
2. 只纳入高置信、可运营解释的 Quest 关系。
3. 产出可以直接执行的 proposal / design / tasks / spec，供后续实现使用。
4. 显式约束歧义处理，避免把低置信链接包装成事实。

## Non-Goals

- 不做全量 Quest encyclopedia。
- 不把所有带 `Quest` 字样的表自动纳入默认查询空间。
- 不因为字段同名（尤其是 `TID`）就自动建立关系。
- 不把 `HelpTable`、`TutorialTable`、`BanWordTable`、`Char*`、`QuestCinemaTable`、`QuestSceneTable` 等默认排除表纳入 Quest v1。
- 不把 World / Map / Area / Portal / Event / Instance 当作 Quest v1 默认关系的一部分。
- 不把低置信字段解释（如某些 `Value` 语义）直接输出为确定事实。

## Success Criteria

1. OpenSpec 文档明确 Quest v1 只覆盖以下关系：
   - Quest -> Mission
   - Quest -> Reward
   - Quest -> QuestDrop
   - Quest -> GiveItem
   - Quest -> Prev/Next
2. 默认查询空间中，Quest 只有一个顶层入口：`QuestTable`。
3. Supporting relation tables 仅限 `QuestMissionTable`、`QuestRewardTable`、`QuestDropTable`，以及为解释结果所需的受控 `ItemTable` / `NpcTable`。
4. 文档明确声明：
   - 禁止 full-table scan 作为产品策略；
   - 禁止 same-name `TID` auto-linking；
   - 禁止把低置信关系表述为事实。
