---
title: Hotspot Monitor PRD
status: draft
version: v2.3-draft
created: 2026-08-06
updated: 2026-08-07
product_brief: ../product-brief.md
product_architecture: ./assets/hotspot-monitor-product-architecture.svg
guide: ../../../GUIDE.md
---

# Hotspot Monitor 产品需求文档（PRD）

## 00 文档信息、版本索引与术语表

| 项目 | 内容 |
|---|---|
| 产品 | Hotspot Monitor（热点监控增长运营系统） |
| 产品定位 | 以 Event 为共享对象的公司级事件驱动增长智能与运营平台 |
| 版本 | v2.3-draft |
| 权威输入 | [Product Brief v1.4](../product-brief.md)、[产品模块与业务关系图](./assets/hotspot-monitor-product-architecture.svg)、[文档规范](../../../GUIDE.md) |
| 文档边界 | 定义业务能力、结果、规则与验收，不定义技术组件、接口或部署方案 |
| 首个验证环境 | Predx 内容运营的突发热点响应（Phase 0） |
| 下游使用者 | UX/UI、系统架构、Epics & Stories、实施就绪评审 |
| 权威入口 | 本文件；历史单文件 PRD 仅作归档参考，不再作为需求基线 |

**追溯主链：**`Signal → Candidate Event → Event Card → Opportunity Card → Task Plan → Review Draft / Action Task → Task Receipt → Outcome → Strategy Recommendation`。

| 术语 | 定义 |
|---|---|
| Signal | 外部或内部来源的原始变化信号，如热榜、新闻、社区讨论、活动日历或人工录入。 |
| Candidate Event | 通过突发信号、未来事件预案或二者匹配进入事件形成流程的候选。 |
| Event | 跨团队共享的现实或未来事件根对象。 |
| Event Card | 汇集 Event 边界、事实、关系、热度、风险、窗口和状态的有版本统一档案。 |
| Fact Item / Source Evidence | 分别表示事实声明及其支持证据；事实、热度和价值是独立判断。 |
| Opportunity Card | 对 Event 的目标价值、受众、风险、资源、决策与承接路径的统一档案。 |
| Task Plan | 针对 Opportunity 明确目标、参与策略、渠道、成功标准、资源与风险边界的任务方案。 |
| Review Draft | 基于已核验事实生成、等待人工审核或修订的内容/交付物草稿。 |
| Action Task | 从已审核任务方案拆解出的、由责任人或外部专业系统承接的行动单元。 |
| Task Receipt | 专业执行系统或行动责任人回传的接收、进度、异常或完成信息。 |
| Outcome | 与行动关联的执行、传播、产品、商业、成本或风险结果。 |

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
| 概念实体 | CE-01—CE-15 | `prd-05` |
| 非功能需求 | NFR-01—NFR-10 | `prd-07` |
| 成功指标 | PM-01—PM-10、P0-01—P0-07 | `prd-08` |
| 决策 | D-01—D-11 | `prd-09` |
