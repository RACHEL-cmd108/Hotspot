---
id: SPEC-event-intelligence-contract
companions:
  - signal-event-routing.md
  - output-field-contract.md
sources: []
---

> **Canonical contract.** 本 SPEC 与 `companions:` 中的文件共同构成 Signal→Event 路由、Event Card 和 Event Context Pack 的完整交付合同。本文以当前工作定义为准。

# 事件情报对象与产出合同

## Why

Signal、Event、Response Moment、Event Card 与 Event Context Pack 的边界必须统一，否则系统会把热度误当事实、重复创建 Event、让摘要卡与完整档案字段漂移，并使产品、设计、研发和 Agent 使用不同输入合同。

## Capabilities

- **CAP-1 Signal 语义路由**
  - **intent:** 系统可以依据 Signal 表达的现实含义，将其创建、匹配或路由到正确的热点对象。
  - **success:** 单条充分 Signal 可直接创建或匹配 Event；观点讨论、独立热门内容和信息不足分别进入 Discussion、Hot Content Sample 或 Candidate Event。
- **CAP-2 Event 匹配与去重**
  - **intent:** 系统可以判断新 Signal 是补充已有 Event，还是代表一个新的独立 Event。
  - **success:** 同一核心现实变化复用 Event；新的动作、决定、结果、事实时间、证据链或独立响应窗口创建关联 Event；所有判断可追溯。
- **CAP-3 Event 演化**
  - **intent:** 系统可以在不重复建 Event 的情况下表达新的关注时点与事实进展。
  - **success:** 只有关注度或响应时机变化时形成 Response Moment；事实、证据或状态变化更新 Event 与 Context Pack；实质独立发展创建关联 Event。
- **CAP-4 Event Card 摘要**
  - **intent:** 用户可以在事件看板快速判断一个 Event 是否值得打开。
  - **success:** Event Card 输出 `output-field-contract.md` 规定的全部必需字段、可核验标签及最多三条代表 Evidence，且不承载完整证据与分析。
- **CAP-5 Event Context Pack 完整档案**
  - **intent:** 用户和系统可以使用统一、事实中立的完整 Event 档案进行理解、核验和机会判断。
  - **success:** Context Pack 输出 `output-field-contract.md` 规定的八个固定模块、事实—证据关系、表达边界、数据限制及版本变化。
- **CAP-6 版本与可追溯性**
  - **intent:** 系统可以保留 Event 理解发生实质变化时的历史状态。
  - **success:** 实质变化生成 Context Pack 新版本并提供变化摘要；普通排名或互动波动只刷新实时指标；旧版本及其下游引用不可被静默覆盖。

## Constraints

- Signal、热搜排名、代表帖子、主题圈讨论和传播强度均不当然等于现实事实确认。
- 单个发现来源达到自身门槛即可进入处理，不等待其他来源共同命中；来源门槛决定响应资格，Event 匹配只负责对象归并。
- Event 必须是一项可独立陈述、可被 Evidence 支持的动作、决定、结果或状态变化，不能等同于关键词、帖子、视频或热度条目。
- 标题、关键词、语言、地区、热度、榜单位置或相同人物不能单独作为 Event 合并依据。
- 字段缺失必须保留空值或明确标记数据不足，不得由程序或 Agent 补造。
- Event 生命周期状态与 Fact 确认状态分别保存；活跃 Event 仍可包含待确认或冲突 Fact。
- Event Card 是摘要视图；Event Context Pack 是完整、版本化档案。
- Context Pack 保持事实与事件上下文中立；Operational Opportunity、Angle 和 Social Content Draft 属于派生层。
- 第一阶段 Event 详情不提供开放式 Agent 对话或 Event 直接内容生成入口。

## Non-goals

- 不在本合同重新定义各来源的全部采集算法、账号清单和专项阈值。
- 不将传播热度推断为事实真实性、观点一致性或发布授权。
- 不定义 Opportunity、Angle、内容生成、自动发布或营销执行合同。
- 不引入跨多个 Event 的 Story 实体。
- 不提供无法由来源数据支持的统一热度分、全平台情绪或完整用户画像。

## Success signal

给定一组包含官方发布、重复报道、热搜跃迁、宽泛争议、未确认传闻和独立后续动作的 Signal，系统能稳定路由到正确对象，避免重复 Event，并分别产出字段完整、边界清晰的 Event Card 与版本化 Event Context Pack。

