---
title: Hotspot Monitor 技术架构
status: draft
version: v0.2-prd-2.10-ux-2.0
updated: 2026-08-13
sources:
  - ../product-requirements/prd/prd-00-index.md
  - ../ux-ui/versions/v2.0-module-v3-v13/ux-00-index.md
spine: ../../_bmad-output/planning-artifacts/architecture/architecture-热点监控-2026-08-11/ARCHITECTURE-SPINE.md
---

# Hotspot Monitor 技术架构

本架构服务开发者和开发代理。业务规则以 PRD 为准，交互与页面状态以 UX/UI v2.0 为准；本文件不回写上游文档。

## 架构主链

`Signal / Future Event → Candidate Event → Event Card → Account Response Task → Content Candidate → 人工 X 发布与 URL/失败原因回填 → Performance Result → Optimisation Proposal`

活动策划为独立支线：`Event Card → Marketing Recommendation → 人工启动 → Campaign Case → 3 Campaign Proposals → 导出/外部交接`。

| 文档 | 说明 |
| --- | --- |
| [01 系统上下文与原则](./arch-01-system-context-and-principles.md) | 系统边界、模块与不可变约束。 |
| [02 组件与代码映射](./arch-02-components-and-code-mapping.md) | 应用服务、异步任务和代码归属。 |
| [03 数据架构](./arch-03-data-architecture.md) | 权威数据、关系、版本、审计和状态。 |
| [04 接口与集成](./arch-04-interfaces-and-integrations.md) | 内部命令/事件、X、AI、Google 集成。 |
| [05 安全与运维](./arch-05-security-and-operations.md) | 身份、权限、审计、监控和事件处置。 |
| [06 部署与扩展](./arch-06-deployment-and-scalability.md) | 环境、恢复、容量和上线门禁。 |
| [07 架构决策](./arch-07-architecture-decisions.md) | 可追溯的 AD-1—AD-19。 |
| [08 开放问题与延后决策](./arch-08-open-questions-and-deferred-decisions.md) | 不阻塞 Phase 0 的边界和触发条件。 |

## Phase 0 实现切片

- 每小时用 X API 监听五个地区；合格热点在每个出现地区采集详情前三条来源，并保留实际数量与错误。
- 一个 Event 命中生效响应规则后，对三个预配置 Predx X 账号分别创建至多一个账号响应任务；账号/Skill 不可用则仅该账号异常，不替代，也不阻塞其他账号。
- 每个可用账号的任务由 AI 生成至少三条账号专属候选，完成预检后由运营人员在系统中选择、复制或调整。
- 系统不自动发 X、不使用 Telegram；运营人员人工发布 X，再回填 URL 或失败原因。
- 记录各阶段实际耗时并提供 P50/P95；不实现固定 5/15 分钟 SLA。

## 非目标

Opportunity、参与决策、Task Plan、Telegram 投递、KOL 工作流、私域发送、热点内容/Content Insight 数据源、外部营销实际执行均不属于当前实现。
