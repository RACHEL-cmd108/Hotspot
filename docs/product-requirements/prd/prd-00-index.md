---
title: Hotspot Monitor PRD — Module v3 Alignment
status: draft
version: v2.10-module-v3-v12-draft
created: 2026-08-06
updated: 2026-08-13
product_brief: ../product-brief.md
product_architecture: ./assets/hotspot-monitor-product-architecture-v3.svg
guide: ../../../GUIDE.md
---

# Hotspot Monitor 产品需求文档（PRD）

## 00 文档信息、版本索引与术语表

| 项目 | 内容 |
|---|---|
| 产品 | Hotspot Monitor（热点内容运营系统） |
| 产品定位 | 帮助运营人员发现热点、形成 Event 上下文并更快产出账号专属内容的运营系统。 |
| 版本 | v2.10-module-v3-v12-draft（当前本地工作基线） |
| 权威输入 | [Product Brief v1.5（对齐草案）](../product-brief.md)、[产品模块架构图 v3](./assets/hotspot-monitor-product-architecture-v3.svg)、[概念实体关系图 v12](./assets/hotspot-monitor-conceptual-domain-model-v12.svg)、本地 HTML 原型终稿 v13（尚未同步远端）、[文档规范](../../../GUIDE.md) |
| 文档边界 | 定义业务能力、结果、规则与验收，不定义技术组件、接口或部署方案 |
| 首个验证环境 | Predx 内容运营的突发热点响应（Phase 0） |
| 下游使用者 | UX/UI、系统架构、Epics & Stories、实施就绪评审 |
| 权威入口 | 本文件；历史单文件 PRD 仅作归档参考，不再作为需求基线 |

**热点内容主链：**`热点 Signal / 未来事件 → Candidate Event → 地区来源聚合与 Event Card → 命中内容响应规则 → Account Response Task → Content Candidate → 人工 X 发布与系统链接回填 → Performance Result → Optimisation Proposal`。

**爆款灵感支线（预留）：**保留“热点内容 → 爆款拆解 / 可复刻要素 → Content Insight → 内容生成上下文”的入口与概念边界；暂不定义数据源、爆款判定或拆解字段，也不纳入当前实施范围。

**活动策划支线：**`Event Card（首版优先 Future Event）→ 受众匹配与综合评估 → 活动准备建议 → 运营人员点击启动 → 3 Campaign Proposal Drafts → 选择、调整、导出/外部交接`。

| 术语 | 定义 |
|---|---|
| Signal | 外部或内部来源的原始变化信号，如热榜、新闻、社区讨论、活动日历或人工录入。 |
| Hot Content / Content Insight（热点内容 / 内容洞察） | 预留的热点具体内容与爆款拆解能力窗口。它不等于热搜 Topic 或 Event；未来可关联 Event 或作为内容灵感，当前不定义数据源、判定口径或拆解字段。 |
| Candidate Event | 通过突发信号、未来事件预案或二者匹配进入事件形成流程的候选。 |
| Event | 跨团队共享的现实或未来事件根对象。 |
| Fact | 可核验的事实声明；与 Event 关联，并由 Evidence 支持、质疑或排除。 |
| Evidence | 支持或质疑 Fact 的来源材料；事实、热度和价值是独立判断。 |
| Event Card | 汇集并呈现 Event、Fact、Evidence、热度、风险、窗口和状态的事件工作台读模型；它不改变这些对象的实体边界，也不承担“是否参与”的决策。 |
| Account Response Task（账号响应任务） | 一个承接账号对一个 Event 的最小内容响应单元，承载账号专属候选、选择、调整、人工发布与链接回填；Phase 0 对三个预配置 Predx X 账号分别匹配。 |
| Content Candidate / Campaign Proposal | 分别是账号专属内容候选与活动方案；内容候选不能跨账号互换，活动方案可比较、调整和导出。 |
| Execution Account（承接账号） | 由生效响应规则匹配，或由运营人员在未来事件预热中选择的明确执行账号；其角色、可用状态和风险边界受配置治理。 |
| Content Skill | 定义一个承接账号的内容角色、表达边界、格式偏好和适用风险规则；用于生成该账号专属候选。 |
| Marketing Recommendation | 基于 Event Card（首版优先关联 Future Event）的确认度、时间窗口、受众、影响范围及生效推荐规则生成的“建议做营销准备”对象；推荐不等于自动立项，须由运营人员点击启动。 |
| Publication Record | 运营手动发布后回填的实际 URL 或失败原因；它不等于传播效果。 |
| Performance Result | 与发布记录关联的传播、账号表现和数据状态。 |
| Optimisation Proposal | 基于 Evaluation Report 和复盘形成、经批准后可反馈到监测、响应、账号/Skill 或活动建议规则的优化建议。 |

## 01 产品愿景与目标

定义完整产品的愿景、当前产品目标和成功定义；Phase 0 仅用于验证，不缩窄全局边界。

详见：[prd-01-product-vision-and-goals.md](./prd-01-product-vision-and-goals.md)。

## 02 用户与旅程

定义核心运营用户、JTBD，以及从监测核验、内容响应、未来营销准备到规则优化的稳定用户旅程 `UJ-1` 至 `UJ-5`。

详见：[prd-02-users-and-journeys.md](./prd-02-users-and-journeys.md)。

## 03 范围与产品能力

以产品架构图的 M1–M5 为产品能力结构，明确完整产品范围、Phase 0 切片、外部执行系统边界与非目标。

详见：[prd-03-scope-and-capabilities.md](./prd-03-scope-and-capabilities.md)。

## 04 功能需求

定义 `FR-01` 至 `FR-25`；每条需求包含关联旅程、角色、触发条件、行为、边界和可测试结果。

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
| 功能需求 | FR-01—FR-25 | `prd-04` |
| 概念实体 | E01—E17 | `prd-05` |
| 非功能需求 | NFR-01—NFR-11 | `prd-07` |
| 成功指标 | PM-01—PM-10、P0-01—P0-09 | `prd-08` |
| 决策 | D-01—D-27 | `prd-09` |
