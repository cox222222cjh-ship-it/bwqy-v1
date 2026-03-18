# Proposal: add-operator-query-regression-sample-suite

## Why
当前 Item / NPC / Quest / unified-backend 已经形成可复用的运营查询基线，但代表性验收样本仍分散在各模块测试里，且大多是手写伪数据。后续 PR 在修改查询逻辑或白名单路径时，容易因为缺少“真实数据样本 + 稳定不变量”而在评审阶段反复补解释。

## What Changes
- 新增一份基于当前仓库真实表数据挑选的运营查询回归样本池。
- 为 Item / NPC / Quest / unified routing 增加可复用的集成式回归测试。
- 在文档中明确样本的代表性、验证的白名单路径/产品规则、以及未来 PR 如何复用这套样本。

## Non-goals
- 不扩展新的查询域。
- 不修改 UI 表现层。
- 不扩大现有白名单边界。
- 不引入全表浏览器或低置信自动推断。
