# Design: add-operator-query-regression-sample-suite

## Baseline
本 change 以前，当前基线已支持：
- Item 精确/重名/装备套装链查询。
- NPC 商店/掉落及 Item 反向来源查询。
- Quest 主记录、give-item、reward、quest-drop、prev/next、向量字段保守处理。
- unified backend 对 Item / NPC / Quest 的最小路由与歧义返回。

## Design Decisions
1. **样本来源必须是真实表数据**
   - 样本从当前仓库 checked-in CSV 表中挑选。
   - 测试只断言稳定不变量，不做脆弱的全文快照。

2. **样本池单独建模**
   - 用单独的 Python 样本模块承载查询、期望域、关键 TID/名称、对应规则说明。
   - 文档层用 markdown 解释样本意义与维护流程。

3. **按域分层验收**
   - Item / NPC / Quest / Unified 各自有 focused regression assertions。
   - unified 层复用相同样本，验证 no-hint / domain_hint / ambiguity / not_found 等路由约束。

## Invariants
- 不做 full-table scanning 作为产品能力。
- 不做 same-name TID auto-linking。
- 不做低置信 relation inference。
- 不扩大 whitelist boundaries。
- 测试只校验 domain、status、关键 ID/名称、白名单路径与保守歧义行为。
