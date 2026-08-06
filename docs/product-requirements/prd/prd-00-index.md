---
title: Hotspot Monitor PRD
status: draft
version: v2.2
created: 2026-08-06
updated: 2026-08-06
product_brief: ../product-brief/current/product-brief-v1.3.md
product_architecture: ../system-design/product-architecture/hotspot-monitor-product-architecture.svg
guide: ../../../GUIDE.md
---

# Hotspot Monitor 产品需求文档（PRD）

## 00 文档信息、版本索引与术语表

| 项目 | 内容 |
|---|---|
| 产品 | Hotspot Monitor（热点监控增长运营系统） |
| 产品定位 | 以 Event 为共享对象的公司级事件驱动增长智能与运营平台 |
| 版本 | v2.1 / draft |
| 权威输入 | [Product Brief v1.3](../product-brief/current/product-brief-v1.3.md)、[产品模块与业务关系图](../system-design/product-architecture/hotspot-monitor-product-architecture.svg)、[文档规范](../../../GUIDE.md) |
| 文档边界 | 定义业务能力、结果、规则与验收，不定义技术组件、接口或部署方案 |
| 首个验证环境 | Predx 内容运营的突发热点响应（Phase 0） |
| 下游使用者 | UX/UI、系统架构、Epics & Stories、实施就绪评审 |
| 权威入口 | 本文件；历史单文件 PRD 仅作归档参考，不再作为需求基线 |

**追溯主链：**`Signal → Candidate Event → Event Card → Opportunity Card → Action Package → Execution Result → Outcome → Strategy Recommendation`。

| 术语 | 定义 |
|---|---|
| Signal | 外部或内部来源的原始变化信号，如热榜、新闻、社区讨论、活动日历或人工录入。 |
| Candidate Event | 通过突发信号、未来事件预案或二者匹配进入事件形成流程的候选。 |
| Event / Event Card | 对现实或未来事件的共享业务对象及其有版本的统一档案。 |
| Fact Item / Source Evidence | 分别表示事实声明及其支持证据；事实、热度和价值是独立判断。 |
| Opportunity Card | 对 Event 的目标价值、受众、风险、资源、决策与承接路径的统一档案。 |
| Action Package | 已决定参与的机会所生成的跨团队、跨执行系统任务包。 |
| Outcome | 与行动关联的执行、传播、产品、成本或风险结果。 |

## 01 产品愿景与目标

定义完整产品的愿景、当前产品目标和成功定义；Phase 0 仅用于验证，不缩窄全局边界。

详见：[prd-01-product-vision-and-goals.md](./prd-01-product-vision-and-goals.md)。

## 02 用户与旅程

定义多团队用户、JTBD，以及从发现、判断、执行到学习的稳定用户旅程 `UJ-1` 至 `UJ-5`。

详见：[prd-02-users-and-journeys.md](./prd-02-users-and-journeys.md)。

## 03 范围与产品能力

以产品架构图的 M1–M5 为产品能力结构，明确完整产品范围、Phase 0 切片、外部执行系统边界与非目标。

详见：[prd-03-scope-and-capabilities.md](./prd-03-scope-and-capabilities.md)。

## 04 功能需求

定义 `FR-01` 至 `FR-26`；每条需求包含关联旅程、角色、触发条件、行为、边界和可测试结果。

详见：[prd-04-functional-requirements.md](./prd-04-functional-requirements.md)。

## 05 概念领域模型

定义业务实体、关系、生命周期和关键业务事件，并建立能力、旅程和功能需求到实体的映射；不涉及数据表或技术存储。

详见：[prd-05-conceptual-domain-model.md](./prd-05-conceptual-domain-model.md)。

## 06 业务与数据规则

定义事实和风险治理、状态流转、权限、外部回执和数据口径约束；实体关系以概念领域模型为准。

详见：[prd-06-business-and-data-rules.md](./prd-06-business-and-data-rules.md)。

## 07 非功能需求

定义性能、可靠性、审计、安全、兼容性和可访问性的可测量产品要求。

详见：[prd-07-non-functional-requirements.md](./prd-07-non-functional-requirements.md)。

## 08 指标与实验

定义产品级指标框架与 Phase 0 的明确验证指标、样本与反向指标，避免以内容 MVP 指标替代全局价值。

详见：[prd-08-metrics-and-experiments.md](./prd-08-metrics-and-experiments.md)。

## 09 决策与开放问题

记录影响范围的产品决策、已知假设、依赖、风险和开放问题，并区分是否阻塞进入 UX/UI。

详见：[prd-09-decisions-and-open-questions.md](./prd-09-decisions-and-open-questions.md)。

## 跨文档追踪

| 类型 | 范围 | 权威位置 |
|---|---|---|
| 用户旅程 | UJ-1—UJ-5 | `prd-02` |
| 功能需求 | FR-01—FR-26 | `prd-04` |
| 概念实体 | CE-01—CE-13 | `prd-05` |
| 非功能需求 | NFR-01—NFR-10 | `prd-07` |
| 成功指标 | PM-01—PM-06、P0-01—P0-07 | `prd-08` |
| 决策 | D-01—D-09 | `prd-09` |
