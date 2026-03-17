# Spec: item-query-v1

## ADDED Requirements

### Requirement: Item Query Entry

系统 SHALL 提供一个仅面向物品的查询入口，支持使用物品名称或物品 ID 发起查询。查询结果 MUST 首先尝试命中物品主表记录。

#### Scenario: Search by item name
- Given 用户输入一个物品名称
- When 系统执行查询
- Then 系统返回匹配的物品主表记录或候选列表

#### Scenario: Search by item ID
- Given 用户输入一个物品 ID
- When 系统执行查询
- Then 系统返回对应的物品主表记录

### Requirement: Trusted Base Information

系统 MUST 基于物品主表展示该物品的基础信息。基础信息 SHALL 至少包括物品名称、物品 ID、分类，以及主表中可直接确认的关键字段。

#### Scenario: Base info display
- Given 系统已命中一个物品主表记录
- When 页面渲染结果
- Then 页面显示该物品的基础信息
- And 页面不得展示无法确认的基础字段为“确定值”

### Requirement: Equipment Chain Display

如果该物品被识别为装备，系统 MUST 展示最关键的装备链路信息。该链路 SHALL 只要求覆盖第一版中确定性最高、最常用的部分，不要求全量覆盖所有装备关联。

#### Scenario: Equipment item
- Given 命中的物品被判定为装备
- When 页面渲染结果
- Then 页面显示装备链路信息
- And 页面说明链路信息来自哪些表和字段

#### Scenario: Non-equipment item
- Given 命中的物品不是装备
- When 页面渲染结果
- Then 页面不显示装备链路区域或明确标识“不适用”

### Requirement: Traceability

系统 MUST 让展示的每个结果项支持追溯。系统 SHALL 至少说明来源表、来源字段，以及该值属于直接读取还是推断结果。

#### Scenario: Direct field
- Given 一个字段可直接从主表读取
- When 页面展示该字段
- Then 页面标明来源表与来源字段
- And 页面标记其为“直接读取”

#### Scenario: Derived field
- Given 一个字段需要通过关联或规则推导
- When 页面展示该字段
- Then 页面标明来源链路
- And 页面标记其为“推断”

### Requirement: Uncertain Result Handling

系统 MUST 不得把不确定结果表现为确定事实。任何无法充分确认的字段、链路或分类，系统 SHALL 显式标记为“待确认”。

#### Scenario: Uncertain association
- Given 某关联链路存在证据不足
- When 页面展示结果
- Then 页面显示“待确认”
- And 页面不得隐去该不确定性