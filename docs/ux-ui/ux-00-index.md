---
title: Hotspot Monitor UX/UI
status: draft
version: v1.6
updated: 2026-08-11
prd: ../product-requirements/prd/prd-00-index.md
product_architecture: ../product-requirements/system-design/product-architecture/hotspot-monitor-product-architecture-m4-integrated.svg
---

# Hotspot Monitor UX/UI 设计

## 00 文档信息、版本与旅程映射

| 项目 | 内容 |
|---|---|
| 设计范围 | 完整定义 M1–M5；Phase 0 深化内容运营的突发热点响应，完整产品保留四类 M4 行动设计 |
| 产品形态 | 内部多角色、桌面优先 Web 工作台；1440px 主画布，1280px 最低完整工作宽度 |
| 工作台层次 | 同一工作台提供“我的响应台（Phase 0 默认）”与“全局运营台（完整产品）”，系统记忆用户选择 |
| Phase 0 | 成功小时采集中的合格触发（`T0`）→ 自动形成/更新 Candidate Event、Event / Event Card；策略在 Opportunity 写入“参与”并生成内容型 Task Plan → 自动选入内容发布行动 → 5 分钟内生成并规则预检至少 3 条普通社媒内容候选 → Telegram 内部投递 → 内容运营 15 分钟内选择一条、人工发布并回填链接；高风险内容另走人工审核 |
| M4 能力 | 内容发布、营销活动、私域触达、KOL 合作；Task Plan 用四张渠道行动卡协调建议、选择、依赖、影响分析和重规划，统一任务中心承接后续交付 |
| 权威规则 | 系统内部保存交付物、自动触发/预检、选择、审核和状态；Telegram、Google Docs、X 等均为可替换连接器 |
| 本轮修订 | 已同步页面系统、逐页规格、流程、状态、组件、无障碍与验收；已交付 17 页低保真线框、核心路径高保真参考和覆盖 17 页入口的 v2 可点击原型。剩余工作是补充代表状态视觉稿与原型无障碍实现，而非重绘整套资产。 |
| 页面约定 | `PG` 为可深链页面，`VW` 为页面内视图，`OV` 为弹层/抽屉，`CP` 为可复用组件；以第 02、04 章为准 |

### PRD 用户旅程映射

| 旅程 | UX 流程 | 核心页面 | 深化程度 |
|---|---|---|---|
| UJ-1 突发热点发现 | UX-F01、UX-F04 | PG-02A、PG-03、PG-04、PG-07 | Phase 0 优先 |
| UJ-2 未来事件准备 | UX-F03 | PG-05、PG-04、PG-07 | 完整产品 |
| UJ-3 事件理解与机会决策 | UX-F04、UX-F05 | PG-07—PG-09 | Phase 0 优先 |
| UJ-4 多类型行动与执行协同 | UX-F02、UX-F06—UX-F10 | PG-09—PG-12、PG-14、PG-16 | 内容链为 Phase 0；其余为完整产品 |
| UJ-5 结果学习与策略反馈 | UX-F11 | PG-13、PG-06、PG-08、PG-09 | 完整产品 |

### 追溯主链

`Signal → Candidate Event → Event → Event Card → Opportunity Card → Task Plan → Execution Deliverable Draft → Action Task → Task Receipt → Outcome → Strategy Recommendation`

## 01 设计目标与基础

定义可信、高密度、自动化优先且保留人工选择/高风险门禁的体验。

详见：[ux-01-design-goals-and-foundations.md](./ux-01-design-goals-and-foundations.md)。

## 02 信息架构

定义共享导航、页面/视图/弹层边界、统一任务中心、四类行动视图、对象链和术语。

详见：[ux-02-information-architecture.md](./ux-02-information-architecture.md)。

## 03 用户流程

覆盖 UJ-1—UJ-5、Opportunity 四档决定、Task Plan 四渠道协同，以及内容、私域、营销、KOL 四条执行链和恢复路径。

详见：[ux-03-user-flows.md](./ux-03-user-flows.md)。

## 04 页面与线框图

定义 17 张可深链页面的目标、范围、逐页规格和跳转边界；第 4.6 节已登记低保真、高保真与 v2 可点击原型的覆盖范围。

详见：[ux-04-pages-and-wireframes.md](./ux-04-pages-and-wireframes.md)。

## 05 交互与状态

定义 Opportunity 决策、Task Plan 版本、渠道选择与重规划、规则预检、人工选择、高风险审核、人工交接、Bot 发送、KOL 私信和回执。

详见：[ux-05-interaction-and-states.md](./ux-05-interaction-and-states.md)。

## 06 视觉设计与组件

定义设计变量、高密度布局、审核/风险语法、渠道行动卡、依赖/影响分析和计划版本组件。

详见：[ux-06-visual-design-and-components.md](./ux-06-visual-design-and-components.md)。

## 07 无障碍与验收

定义代表任务、渠道组合变更验收、逐条 FR 追溯、连接器降级和 UX 门禁。

详见：[ux-07-accessibility-and-validation.md](./ux-07-accessibility-and-validation.md)。
