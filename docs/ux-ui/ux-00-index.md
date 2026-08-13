---
title: Hotspot Monitor UX/UI — Module v3 Alignment
status: draft
version: v2.0-module-v3-v13-draft
created: 2026-08-13
prd: ../product-requirements/prd/prd-00-index.md
prototype: ./prototype/hotspot-operations-system-final-prototype.html
previous_ux: ./archive/versions/v1.8/ux-00-index.md
---

# Hotspot Monitor UX/UI 设计

## 00 文档信息、版本与旅程映射

| 项目 | 内容 |
|---|---|
| 本版范围 | 对齐 PRD v2.10-module-v3-v12-draft 与 HTML 原型终稿 v13；作为主文件树中的当前 UX/UI 基线，旧版已移入本地 archive。 |
| 产品形态 | 内部桌面优先 Web 工作台；共享页面骨架，角色影响操作权限而非页面集合。 |
| 一级导航 | 运营总览、热点监测、运营排期、事件管理、内容发布、复盘优化、系统设置。 |
| 核心主链 | Signal / Future Event → Candidate Event → 地区来源聚合与 Event Card → 账号响应任务 → Content Candidate → 人工 X 发布与 URL 回填 → Performance Result → Optimisation Proposal。 |
| 并行支线 | Event Card → 活动准备建议 → 运营主动启动 → 3 套 Campaign Proposal → 选择、调整、导出/外部交接。 |
| Phase 0 | X 五地区热搜、每地区详情前三条来源、三个预配置 Predx X 账号各自至少三条候选、系统内选择/复制/调整、X 手动发布与 URL/失败原因回填。 |
| 原型与一期实现的关系 | HTML 原型用于展示完整产品链路和未来页面关系；一期只接通已确认的 Phase 0 内容响应链。原型中展示的多账号、热点内容或其他后续链路，不等于一期承诺。 |
| 明确不在当前链 | Opportunity、参与/不参与决策、Task Plan、Telegram 投递、KOL 工作流、私域发送与社群管理。 |
| 预留能力 | 热点内容、爆款拆解、Content Insight、私域话题讨论建议；未定义输入和输出前必须显示为未启用能力。 |

## 01 设计目标与基础

本章定义桌面工作台的设计原则、用户职责、自动化边界和术语规范。

详见：[ux-01-design-goals-and-foundations.md](./ux-01-design-goals-and-foundations.md)。

## 02 信息架构

本章定义七个一级页面、页面内视图、对象工作区及关键跳转，确保模块能力与运营页面名称不混淆。

详见：[ux-02-information-architecture.md](./ux-02-information-architecture.md)。

## 03 用户流程

本章定义 UJ-1—UJ-5 的端到端流程、活动策划并行支线、预留能力边界与恢复路径。

详见：[ux-03-user-flows.md](./ux-03-user-flows.md)。

## 04 页面与线框规格

本章定义每页回答的问题、必备信息、操作边界、页面间跳转和与 v13 原型的覆盖关系。

详见：[ux-04-pages-and-wireframes.md](./ux-04-pages-and-wireframes.md)。

## 05 交互与状态

本章定义 Candidate Event、Event、账号响应任务、内容候选、发布记录、活动方案和优化建议的状态、门禁与异常恢复。

详见：[ux-05-interaction-and-states.md](./ux-05-interaction-and-states.md)。

## 06 视觉设计与组件

本章提炼终稿原型的视觉语言和可复用组件，规定来源、确认度、风险、预留能力和版本的表达方式。

详见：[ux-06-visual-design-and-components.md](./ux-06-visual-design-and-components.md)。

## 07 无障碍与验收

本章定义桌面 Web 可访问性底线、代表任务、状态覆盖与 FR/NFR 追溯。

详见：[ux-07-accessibility-and-validation.md](./ux-07-accessibility-and-validation.md)。

## 基线与历史

- 当前交互和视觉参考：[HTML 原型终稿 v13](./prototype/hotspot-operations-system-final-prototype.html)。
- 当前上游需求基线：[PRD v2.10 module v3](../product-requirements/prd/prd-00-index.md)。
- 旧版 UX/UI 已移入本地 `archive/versions/v1.8/`。它基于旧的四渠道 Task Plan 模型，不能作为本版开发依据，也不会同步远端。

## 设计资产与验收状态

| 资产 | 用途 | 权威位置 |
|---|---|---|
| 信息架构图 | 七个一级页面、工作区与对象流转 | [ux-information-architecture-v2.0.svg](./assets/ux-information-architecture-v2.0.svg) |
| 关键页面低保真线框 | PG-01—PG-07 的稳定区域与跨页关系 | [ux-page-wireframes-v2.0.svg](./assets/ux-page-wireframes-v2.0.svg) |
| 七个一级页面高保真图 | 当前视觉与页面布局基线 | [PG-01](./assets/hifi-01-operations-overview.svg) · [PG-02](./assets/hifi-02-hotspot-monitoring.svg) · [PG-03](./assets/hifi-03-operations-schedule.svg) · [PG-04](./assets/hifi-04-event-management.svg) · [PG-05](./assets/hifi-05-content-publishing.svg) · [PG-06](./assets/hifi-06-insights-optimization.svg) · [PG-07](./assets/hifi-07-system-configuration.svg) |
| 可点击高保真 | 完整链路的交互与视觉演示；不等于一期全部接通 | [HTML 原型终稿 v13](./prototype/hotspot-operations-system-final-prototype.html) |
| 页面状态覆盖与验证 | 默认、等待、空、异常、受限状态及实际测试记录 | [ux-07-accessibility-and-validation.md](./ux-07-accessibility-and-validation.md) |

当前状态：**设计规格待验证**。页面资产、状态和验收要求已登记；真实浏览器、键盘和代表任务的执行记录尚待补充，未完成前不能标记为“开发验收通过”。
