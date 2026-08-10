# UX/UI 文档审查 — Hotspot Monitor

- **审查方式：**BMad UX Validate（规范覆盖 / 交接形态镜头）
- **审查范围：**`docs/ux-ui/`，并以 PRD v2.4-draft 为需求基线
- **审查日期：**2026-08-10
- **审查限制：**只读；未修改任何现有 UX 文档、原型或视觉资产。

## 总体结论

现有文档已经清楚表达了产品的主对象链、双层工作台、四类行动的不同自动化边界，以及 Telegram 的“内部审核目标”定位；它是有价值的产品/设计讨论底稿。但它尚不是可由架构、Story 和前端直接稳定提取的 UX 合同：核心流程和页面规格仍以摘要文字为主，M1/M2 的状态与页面边界没有封口，设计 token、组件行为和视觉资产之间也没有一个单一权威来源。

按 `GUIDE.md` 的 UX/UI 门禁，以及 BMad UX 的交付形态要求，结论为 **待整改**。先补“页面—流程—状态—组件”的可追溯合同，再更新高保真，能以最低返工成本消除当前阻塞。

## 1. 流程覆盖 — broken

已核对 PRD 的 `UJ-1`—`UJ-5` 与 [ux-03-user-flows.md](./ux-03-user-flows.md)。只有 `UX-F01` 有流程图；其余主流程以一两段文字或一行对象链表示。没有一条流程以可测试的形式同时定义主要角色、编号步骤、关键决策、失败分支、恢复入口和完成条件。

### 发现

- **[critical]** `UJ-1`—`UJ-5` 没有逐条成为可实施的 UX 流程。`UX-F02`—`UX-F11` 主要是内联对象链或段落，`UJ-2`、`UJ-5` 没有图，`UJ-1` 与 `UJ-3` 也被混在 `UX-F01/F04` 中。([ux-03-user-flows.md:3-60](./ux-03-user-flows.md:3)) 这不满足 `GUIDE.md` 对“核心流程、关键分支、异常和恢复路径均有流程图”的要求。*修复：*为 `UJ-1` 至 `UJ-5` 各建立一张主流程图；每张包含角色泳道或明确主体、输入/输出对象、决策点、完成态，以及失败后指向相应 `UX-R` 的连线。

- **[high]** 恢复路径是一个无连接关系的表，无法判断哪一条主流程必须覆盖哪一条异常，也无法确定恢复后的对象状态。([ux-03-user-flows.md:62-74](./ux-03-user-flows.md:62)) *修复：*给每个 `UX-R` 增加“来源流程 / 触发状态 / 恢复后状态 / 是否需重新审核”字段，并在相应 Mermaid 图中画出分支。

- **[high]** `UX-F01` 把 Candidate、Event、Event Card、Opportunity 和 Task Plan 压缩为一条直线，遗漏 PRD 要求的重复处置、证据不足留在监测、四档机会决策中的“观察/不参与”、以及人工发布无回执后的回流。([ux-03-user-flows.md:5-16](./ux-03-user-flows.md:5), [prd-02-users-and-journeys.md:24-60](../product-requirements/prd/prd-02-users-and-journeys.md:24)) *修复：*将其仅保留为 Phase 0 happy path；另外为 UJ-1、UJ-3 绘制完整决策流，并用稳定状态名称而非只用页面名。

- **[medium]** 标题编号重复：`UX-F11` 和“恢复路径”都写为 `3.11`。([ux-03-user-flows.md:58-62](./ux-03-user-flows.md:58)) *修复：*恢复路径顺延为 `3.12`，并在索引增加恢复流程引用。

## 2. Token 完整性 — broken

`ux-06` 给出了有限的色值和圆角值，实际图稿也能复用这组颜色；但没有 BMad 所要求的 `DESIGN.md` 视觉主合同，也没有 YAML token 层、语义 token 层、token 引用语法或可验证的对比度组合。

### 发现

- **[critical]** `docs/ux-ui/` 中不存在 `DESIGN.md`；所有视觉决策散落在 [ux-01-design-goals-and-foundations.md:39-45](./ux-01-design-goals-and-foundations.md:39) 和 [ux-06-visual-design-and-components.md:3-19](./ux-06-visual-design-and-components.md:3)。下游实现者无法判定哪一处是视觉权威，也无法机器提取 token。*修复：*新增 `DESIGN.md`，含 `sources`、YAML tokens（颜色、字号、间距、圆角、组件），并在正文按 BMad 顺序写 Brand & Style → Colors → Typography → Layout & Spacing → Elevation & Depth → Shapes → Components → Do's and Don'ts。

- **[high]** token 只覆盖 10 个基础颜色和 3 个圆角，缺少字体族、字重层级、行高、间距刻度、阴影/层级、focus/disabled/selected/hover 状态、图表系列和语义别名；`44px` 行高、`240px` 导航等数值则以散文散落。([ux-06-visual-design-and-components.md:5-19](./ux-06-visual-design-and-components.md:5), [ux-06-visual-design-and-components.md:59-65](./ux-06-visual-design-and-components.md:59)) *修复：*将可复用量值统一移入 token；用如 `{color.status.warning.fg}`、`{spacing.4}`、`{component.table.row.compact}` 的引用，页面文档不再另写魔法数。

- **[medium]** 文档宣称符合 WCAG 2.2 AA，但未指定哪些前景/背景组合属于“承重组合”，也没有最小对比度或验证方法。([ux-07-accessibility-and-validation.md:3-10](./ux-07-accessibility-and-validation.md:3)) *修复：*在视觉合同中列出正文、次要文字、按钮、状态标签和图表线条的前景/背景 token 对及对比度目标。

## 3. 组件覆盖 — thin

`CP-01`—`CP-24` 是有用的组件目录，但多数条目只有一个名词短语，缺少独立的视觉、结构、行为、状态、权限和无障碍规则。它不能稳定约束高保真、HTML 原型和后续组件实现。

### 发现

- **[high]** 24 个组件没有“一组件一合同”。例如雷达、时间轴、Event 监测图和 Evidence 抽屉只规定展示字段，未规定筛选/排序、钻取、数据过期、加载、空、键盘操作、读屏摘要或权限降级。([ux-06-visual-design-and-components.md:30-57](./ux-06-visual-design-and-components.md:30)) *修复：*在 `DESIGN.md.Components` 中定义每个组件的视觉结构和 token；在 `EXPERIENCE.md` 或现有行为文档中为每个组件定义触发、输入、状态、失败、权限、键盘/读屏规则和所属页面。

- **[high]** `CP-21`—`CP-24` 已加入目录，但没有对应的正式高保真资产或登记为“spine-only”；Phase 0 高保真覆盖声明反而称覆盖 `PG-03`。([ux-06-visual-design-and-components.md:54-57](./ux-06-visual-design-and-components.md:54), [ux-04-pages-and-wireframes.md:30-33](./ux-04-pages-and-wireframes.md:30)) *修复：*在每个组件行增加“已图稿化 / 仅规则化”状态及资产链接；待后续画图前，先完成其行为规格，避免把 HTML 演示误当成正式资产。

- **[medium]** 对象链组件使用非规范简称 `Deliverable Draft`、`Receipt`，而 PRD 的权威术语为 `Execution Deliverable Draft`、`Task Receipt`。([ux-06-visual-design-and-components.md:36](./ux-06-visual-design-and-components.md:36), [prd-00-index.md:25-28](../product-requirements/prd/prd-00-index.md:25)) *修复：*保留界面友好中文“交付物草稿 / 任务回执”，但在所有规格、组件名、图稿说明中统一写完整英文技术名或建立正式别名表。

## 4. 状态覆盖 — thin

M4 的 `Task Plan`、`Execution Deliverable Draft`、`Action Task` 和 `Task Receipt` 生命周期被正确分开，是当前文档最成熟的一部分；但这只覆盖了概念模型中的一部分对象。页面基础状态是通用规则，不是“页面 × 状态 × 操作”的实施矩阵。

### 发现

- **[critical]** M1/M2/M5 的核心对象没有可执行的状态合同：Monitoring Scope、Signal、Future Event、Candidate Event、Event、Fact、Evidence、Event Card、Opportunity、Outcome、Strategy Recommendation 的生命周期均未在 UX 状态文档中落地。([ux-05-interaction-and-states.md:7-14](./ux-05-interaction-and-states.md:7), [prd-05-conceptual-domain-model.md:7-25](../product-requirements/prd/prd-05-conceptual-domain-model.md:7)) *修复：*按 PRD 生命周期补全对象状态矩阵，逐项写明状态标签、允许动作、角色、下一状态、异常/恢复、是否会使下游草稿或任务过期。

- **[high]** `PG-02A—PG-17` 被笼统声明覆盖默认、加载、空、成功、失败、部分成功、权限受限，但未定义每个页面具体有哪些状态或其文案和可用动作。([ux-07-accessibility-and-validation.md:27-29](./ux-07-accessibility-and-validation.md:27), [ux-05-interaction-and-states.md:57-67](./ux-05-interaction-and-states.md:57)) *修复：*建立页面状态矩阵；例如 PG-03 必须包含“无 Signal、筛选无结果、来源延迟、来源不可用、无权限查看来源、Candidate 已合并”，PG-16 必须包含“改期、取消、窗口到达、匹配不足”。

- **[high]** 现有高保真将 Action Task 主状态写作“待执行”，与 PRD 和 UX 主状态表规定的“待交接”不一致，易导致接口和看板统计出现一套额外状态。([assets/hifi-task-receipts.svg:1](./assets/hifi-task-receipts.svg:1), [ux-05-interaction-and-states.md:9-14](./ux-05-interaction-and-states.md:9)) *修复：*将资产与原型中所有“待执行”替换为“待交接”，或在 PRD 变更后才引入该状态；不得把交接门禁隐含为执行态。

- **[medium]** 文档没有定义 component focus、hover、disabled、readonly、pending confirmation 等交互状态；“基础状态”也未提及离线/网络断开，尽管多个页面依赖来源和连接器。([ux-05-interaction-and-states.md:57-67](./ux-05-interaction-and-states.md:57)) *修复：*增加组件状态表与连接器/来源网络状态；明确离线时哪些数据可读、哪些动作禁用、如何排队或恢复。

## 5. 视觉参考覆盖 — broken

SVG 文件均可解析，且现有关键图稿与文档链接没有发现失效链接；问题在于“图稿覆盖声明、页面清单和实际资产”不一致，原型又没有成为正式设计资产的一部分。

### 发现

- **[critical]** 文档声称 Phase 0 高保真覆盖 `PG-03—08`，但高保真登记表没有 `PG-03`（热点雷达/候选）资产；现有 `hifi-*` 文件中也没有与 PG-03 对应的正式 SVG。([ux-04-pages-and-wireframes.md:30-33](./ux-04-pages-and-wireframes.md:30), [ux-04-pages-and-wireframes.md:39-52](./ux-04-pages-and-wireframes.md:39)) 这使 M1 的关键入口没有一个被批准的视觉/交互参考。*修复：*先将“PG-03 高保真”改为未覆盖，并登记它需具备的组件和状态；后续再补图。不要以原型 HTML 代替未登记的高保真。

- **[high]** `PG-16` 将 Future Event 与配置/字典合并为一个页面，而 IA 的导航把未来事件列在“热点与事件”、配置列在“配置与字典”；页面地图又把两者合并为 `PG-16 配置/未来事件`。([ux-04-pages-and-wireframes.md:23](./ux-04-pages-and-wireframes.md:23), [ux-02-information-architecture.md:7-12](./ux-02-information-architecture.md:7), [ux-02-information-architecture.md:35-37](./ux-02-information-architecture.md:35)) *修复：*拆成两个稳定 PG ID：Future Event Center（业务工作区）和 Configuration & Dictionary（管理工作区），随后分别建立规格、状态和权限。

- **[medium]** `ux-00` 写“16 类页面、12 类关键高保真”，但 `PG-01`、`PG-02A`、`PG-02B`、`PG-03—17` 共 18 个页面标识，4.3 表列出 14 条高保真链接。([ux-00-index.md:58-60](./ux-00-index.md:58), [ux-04-pages-and-wireframes.md:7-24](./ux-04-pages-and-wireframes.md:7), [ux-04-pages-and-wireframes.md:39-52](./ux-04-pages-and-wireframes.md:39)) *修复：*把范围声明改为准确的页面数与图稿数，并将“关键页面 / 仅规则化页面 / 延后视觉化页面”明确分组。

- **[medium]** [hotspot-monitor-clickable-prototype.html](./prototype/hotspot-monitor-clickable-prototype.html) 与 `hifi-workbench.svg` 都未从任何 UX Markdown 资产表链接；后者尤其是未被引用的旧工作台。*修复：*登记原型的用途、版本、覆盖页面和“spines 优先”的地位；归档或删除（经确认后）未引用的旧工作台，避免实现者从错误参考开始。

## 6. 冗余与过度规定 — adequate

文档总体比冗长更偏摘要，尚未出现妨碍实施的大面积叙述性重复。主要问题不是过度规定，而是把原本必须结构化的决策压缩成短段落，从而造成“看起来覆盖、实际不可执行”。

### 发现

- **[low]** “所有页面有规格”“不同结构均有线框”的陈述大于实际交付：4.1 只有四列清单，未包含每页进入来源、必须内容、操作、成功去向、状态/权限。([ux-00-index.md:22](./ux-00-index.md:22), [ux-04-pages-and-wireframes.md:5-24](./ux-04-pages-and-wireframes.md:5)) *修复：*把断言替换成页面规格矩阵；不要用额外说明性段落填补缺项。

## 7. 继承纪律与术语 — thin

PRD 链接和绝大多数主术语已对齐；但 UX 缺少显式来源清单和术语别名规则，导致页面/流程映射和同一对象名称在组件、资产、原型间仍然发生漂移。

### 发现

- **[high]** 没有 BMad 的双主文档与 `sources` frontmatter，也没有明确的“spines 与图稿/原型冲突时谁优先”规则。([ux-00-index.md:1-8](./ux-00-index.md:1), `docs/ux-ui/` 中不存在 `DESIGN.md`、`EXPERIENCE.md`) *修复：*建立这对主文档并以 PRD、Product Brief、产品架构图和当前 UX 索引为来源；在二者各自声明“主文档优先于 SVG/HTML 图稿”。保留现有 00—07 结构作为便于团队阅读的派生/细化文档。

- **[high]** UJ 映射与页面地图的责任边界不一致：`UJ-2` 映射到 `PG-03、PG-16`，但 `PG-03` 的名称把雷达和候选合并、`PG-16` 又把未来事件和配置合并，不能用稳定页面 ID表达 UJ-2 的具体落点。([ux-00-index.md:28-32](./ux-00-index.md:28), [ux-02-information-architecture.md:25-37](./ux-02-information-architecture.md:25)) *修复：*先完成页面 ID 拆分，再将每个 UJ 映射到唯一的页面、流程、状态和验证任务。

- **[medium]** `FR-24` 与 `FR-25` 被错误映射到 `UX-F10`（KOL 合作），而结果学习的正确流程是 `UX-F11`。([ux-07-accessibility-and-validation.md:45-46](./ux-07-accessibility-and-validation.md:45), [ux-03-user-flows.md:54-60](./ux-03-user-flows.md:54)) *修复：*改为 `PG-14、UX-F11`，并将 `FR-21—25` 都补上 Outcome/复盘/策略建议的明确页面状态与验证任务。

## 8. 形态适配 — broken

现有八篇 `ux-00`—`ux-07` 符合项目 `GUIDE.md` 的文件树，且桌面 Web、双工作台、角色和无障碍基线已经提出；但按 BMad UX 的可消费合同标准，缺少 `DESIGN.md` / `EXPERIENCE.md` 两个受控 spine，因此视觉与行为没有统一的上游锚点。

### 发现

- **[critical]** 缺少 `EXPERIENCE.md`，因此 Foundation、Information Architecture、Voice and Tone、Component Patterns、State Patterns、Interaction Primitives、Accessibility Floor、Key Flows 等必备体验合同只能从八篇文档零散拼出。*修复：*新建 `EXPERIENCE.md`，逐段引用 `DESIGN.md` token，作为行为权威；将现有 00—07 的细节链接回它，而不是复制。

- **[medium]** 文档只给出桌面断点，没有定义低于 1280px 时的最低可用策略（阻止、只读、横向滚动、简化布局或明确不支持页面）。([ux-06-visual-design-and-components.md:59-61](./ux-06-visual-design-and-components.md:59)) *修复：*在 Experience 的 Responsive & Platform 中明确每个断点的支持承诺，至少给出窄桌面/窗口缩小时的降级行为。

## 机械检查说明

- 已检查 `docs/ux-ui/assets/*.svg`：XML 均可解析。
- 已检查现有 Markdown 对 SVG 的本地引用：未发现失效引用。
- 发现 1 个未在 UX Markdown 中引用的资产：`assets/hifi-workbench.svg`；可点击 HTML 原型同样未登记。
- `ux-03-user-flows.md` 存在重复章节编号 `3.11`；`ux-00-index.md` 的页面/高保真数量声明与清单不一致。

## 建议整改顺序

1. 先建立 `DESIGN.md` 与 `EXPERIENCE.md` 两个主合同，并明确现有 00—07 文档、SVG、HTML 原型的继承关系。
2. 决定并固定完整产品页面 ID：优先拆开“雷达 / Candidate”“Future Event / 配置”，再为每页补规格矩阵。
3. 逐条补 `UJ-1`—`UJ-5` 流程图及 `UX-R` 分支，随后补全所有 CE 的状态矩阵。
4. 为 CP-01—24 建立视觉与行为双规格，特别先完成 CP-21—24 的状态、无障碍和数据过期规则。
5. 修正追溯与数量错误；将 HTML 原型和已批准 SVG 正式登记。之后再重画缺少的高保真，避免视觉资产继续偏离合同。
