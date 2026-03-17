# Tasks: build-v1-item-query-tool

## Task 1: Freeze MVP Scope ✅

根据当前 GSD 文档，冻结第一版范围，只保留：

- 物品名称 / ID 查询
- 主表基础信息展示
- 装备链路
- 追溯与可信标记

删除或下沉到后续版本的内容包括：

- 任务
- 礼包
- 强化
- 全量相关表位置
- 多业务域入口

## Task 2: Define Source Tables and Fields ✅

列出第一版必须依赖的主表与装备链路表，明确：

- 哪张是物品主表
- 哪些字段参与搜索
- 哪些字段参与分类
- 哪些字段参与装备链路
- 哪些字段可直接展示
- 哪些字段只能标记待确认

## Task 3: Build Local Read Path and Index

实现本地 CSV 读取和最小索引方案，使系统能够：

- 通过名称查询物品
- 通过 ID 查询物品
- 返回稳定候选结果

## Task 4: Build Result View Model

定义结果页展示模型，至少包含：

- 基础信息
- 分类
- 来源信息
- 可信度标记
- 装备链路

## Task 5: Implement Minimal Web UI

实现本地只读网页界面，保证：

- 有输入框
- 有结果区
- 有错误提示
- 有无结果状态
- 有待确认标记

## Task 6: Add Acceptance Cases

添加最小验收样例，覆盖：

- 物品名称命中
- 物品 ID 命中
- 装备类物品结果
- 非装备类物品结果
- 不确定结果的“待确认”显示

## Task 7: Validate Trust Rules

验证页面上所有结果项都满足：

- 有来源
- 有状态
- 不确定项不会被当成确定值输出
