# 软件开发文档规范

> **定位**：本规范定义从产品立项到进入开发所需的最小文档集。文档不是为了留档，而是作为阶段门禁：上一个阶段未通过验收，不得进入下一个阶段。

## 快速导航

- [开发流程](#开发流程)：文档产出与阶段门禁的顺序。
- [目录与命名约定](#目录与命名约定)：文件树、编号规则和 `00-index` 写法。
- [文档清单](#文档清单)：每个阶段必须证明的事项。
- [文档详细说明](#文档详细说明)：各交付物的内容与验收标准。
- [工具使用](#工具使用)：如何使用 BMad 构建与检查文档。
- [判定原则](#判定原则)：通过、待整改和不通过的定义。

## 开发流程

```text
产品定义
  Product Brief → PRD
                    ↓
产品设计
  UX Design → UI Design
                    ↓
方案设计
  System Architecture → Epics & Stories → Implementation Readiness
                                                ↓
开发实施
  Sprint Status → Story → 开发、测试与代码评审
```

> **门禁规则**：任一阶段未通过验收，不得进入下一阶段；下游文档不得静默改变上游已确认的目标、范围或决策。

## 目录与命名约定

### 标准文件树

```text
docs/
├── product-requirements/
│   ├── README.md
│   ├── product-brief.md
│   └── prd/
│       ├── prd-00-index.md              # PRD 索引、版本与需求总览
│       ├── prd-01-product-vision-and-goals.md
│       ├── prd-02-users-and-journeys.md
│       ├── prd-03-scope-and-capabilities.md
│       ├── prd-04-functional-requirements.md
│       ├── prd-05-conceptual-domain-model.md
│       ├── prd-06-business-and-data-rules.md
│       ├── prd-07-non-functional-requirements.md
│       ├── prd-08-metrics-and-experiments.md
│       └── prd-09-decisions-and-open-questions.md
├── ux-ui/
│   ├── ux-00-index.md                  # UX/UI 索引、版本与 PRD 旅程映射
│   ├── ux-01-design-goals-and-foundations.md
│   ├── ux-02-information-architecture.md
│   ├── ux-03-user-flows.md
│   ├── ux-04-pages-and-wireframes.md
│   ├── ux-05-interaction-and-states.md
│   ├── ux-06-visual-design-and-components.md
│   ├── ux-07-accessibility-and-validation.md
│   └── assets/
├── architecture/
│   ├── arch-00-index.md                # 架构索引、版本与需求映射
│   ├── arch-01-system-context-and-principles.md
│   ├── arch-02-components-and-code-mapping.md
│   ├── arch-03-data-architecture.md
│   ├── arch-04-interfaces-and-integrations.md
│   ├── arch-05-security-and-operations.md
│   ├── arch-06-deployment-and-scalability.md
│   ├── arch-07-architecture-decisions.md
│   └── arch-08-open-questions-and-deferred-decisions.md
└── development/
    ├── epics-and-stories.md
    ├── implementation-readiness.md
    ├── sprint-status.yaml
    └── stories/
        └── story-{id}.md
```

### `00-index` 规则

PRD、UX/UI 与架构均采用目录而非单一长文档。各目录的 `*-00-index.md` 是可独立阅读的总目录，而非只含链接的索引。它必须保留完整章节层级；每个子文档对应一个章节，章节中只保留 1–3 句摘要和子文档链接，不重复子文档的详细内容。

> **命名与引用**：主题文件按两位序号排序。跨文件引用使用稳定 ID（例如 `UJ-{id}`、`FR-{id}`、`AD-{id}`），不通过文件序号建立依赖。

`*-00-index.md` 的最小写法如下：

```md
## 01 章节名称

本章简要说明主题和读者应获得的结论；详细规则、图表和完整清单留在子文档中。

详见：[对应子文档](./prefix-01-topic.md)。
```

### `00-index` 章节目录

`*-00-index.md` 必须保留如下章节目录；`00` 为文档信息与全局索引，`01` 起的每一章均按上述格式提供简短摘要和链接。

```text
prd/prd-00-index.md
├── 00 文档信息、版本索引与术语表
├── 01 产品愿景与目标              → prd-01-product-vision-and-goals.md
├── 02 用户与旅程                  → prd-02-users-and-journeys.md
├── 03 范围与产品能力              → prd-03-scope-and-capabilities.md
├── 04 功能需求                    → prd-04-functional-requirements.md
├── 05 概念领域模型                → prd-05-conceptual-domain-model.md
├── 06 业务与数据规则              → prd-06-business-and-data-rules.md
├── 07 非功能需求                  → prd-07-non-functional-requirements.md
├── 08 指标与实验                  → prd-08-metrics-and-experiments.md
└── 09 决策与开放问题              → prd-09-decisions-and-open-questions.md

ux-ui/ux-00-index.md
├── 00 文档信息、版本与旅程映射
├── 01 设计目标与基础              → ux-01-design-goals-and-foundations.md
├── 02 信息架构                    → ux-02-information-architecture.md
├── 03 用户流程                    → ux-03-user-flows.md
├── 04 页面与线框图                → ux-04-pages-and-wireframes.md
├── 05 交互与状态                  → ux-05-interaction-and-states.md
├── 06 视觉设计与组件              → ux-06-visual-design-and-components.md
└── 07 无障碍与验收                → ux-07-accessibility-and-validation.md

architecture/arch-00-index.md
├── 00 文档信息、版本与需求映射
├── 01 系统上下文与原则            → arch-01-system-context-and-principles.md
├── 02 组件与代码映射              → arch-02-components-and-code-mapping.md
├── 03 数据架构                    → arch-03-data-architecture.md
├── 04 接口与集成                  → arch-04-interfaces-and-integrations.md
├── 05 安全与运行                  → arch-05-security-and-operations.md
├── 06 部署与可扩展性              → arch-06-deployment-and-scalability.md
├── 07 架构决策                    → arch-07-architecture-decisions.md
└── 08 延期决策与开放问题          → arch-08-open-questions-and-deferred-decisions.md
```

## 文档清单

| 阶段 | 文档 | 必须证明 | 通过证据 |
|---|---|---|---|
| 产品定义 | `product-brief.md` | 问题真实、用户明确、产品值得做 | 问题依据、目标用户、价值主张、首版边界、可衡量目标 |
| 产品需求 | `prd/` | 团队对“做什么、做到什么程度”没有关键歧义 | 范围与非目标、用户流程、带编号的功能需求、量化非功能需求、成功指标、可测试验收条件 |
| UX/UI设计 | `ux-ui/` | 核心用户任务具有清晰、一致且可实现的交互方案 | 用户旅程、信息架构、用户流程、线框图、高保真设计、组件与状态规范 |
| 技术架构 | `architecture/` | 所有核心需求都有一致、可执行的技术承载方式 | 系统边界、组件与依赖、数据与接口、架构决策、安全与部署方案、需求到架构映射 |
| 任务拆分 | `epics-and-stories.md` | 全部需求已拆成有价值、可排序、可实施的工作单元 | 需求覆盖关系、Epic目标、Story验收条件、依赖顺序、无前向依赖 |
| 实施就绪 | `implementation-readiness.md` | PRD、UX/UI、架构和Story相互一致，开发没有未处理的阻塞项 | 文档版本清单、需求覆盖检查、冲突与风险清单、整改责任人、明确的就绪结论 |
| Sprint启动 | `sprint-status.yaml` | 开发顺序和当前状态可被持续、准确地跟踪 | Epic与Story完整登记、顺序一致、状态合法、无孤立项 |
| Story开发 | `stories/story-{id}.md` | 开发者无需重新猜测需求或架构即可实施 | 来源引用、范围、验收条件、任务、技术约束、依赖和测试要求 |

## 文档详细说明

### `product-brief.md`

**作用**

Product Brief用于判断产品是否值得继续投入，并为PRD提供稳定的方向输入。它应聚焦问题、用户和价值，不展开功能细节或技术方案。

**必须包含**

```text
1. 文档信息
2. 执行摘要
3. 问题与依据
   3.1 核心问题
   3.2 当前解决方式与现状成本
   3.3 用户、业务或研究证据
4. 目标用户与场景
   4.1 主要用户
   4.2 关键使用场景
   4.3 用户目标与预期结果
5. 产品方案与价值
   5.1 产品方案概述
   5.2 核心价值主张
   5.3 与替代方案的差异
6. 首版范围
   6.1 包含范围
   6.2 非范围
7. 目标与成功指标
   7.1 产品目标
   7.2 指标定义与目标值
   7.3 衡量方式
8. 假设、依赖与风险
   8.1 关键假设
   8.2 外部依赖
   8.3 主要风险
9. 开放问题与结论
```

**验收标准**

- [ ] 能用一段话说明产品、目标用户、核心问题和预期价值；
- [ ] 对问题及现状成本有事实、研究或业务依据；
- [ ] 首个版本的范围与非范围清楚；
- [ ] 成功指标有定义、目标值和衡量方式；
- [ ] 关键假设、依赖和风险已公开；
- [ ] 已形成继续进入PRD阶段的明确结论。

### `prd/`

**作用**

PRD定义产品需要实现什么、为什么实现以及做到什么程度，是UX、架构和Story拆分的共同需求基线。PRD描述能力和结果，不指定具体技术实现。为避免单一文档过大，PRD按主题拆分，`prd/prd-00-index.md` 是其唯一入口和版本索引。

**必须包含**

- `prd-00-index.md`：文档信息、版本索引、术语表，以及 UJ、FR、指标和决策的跨文档追踪关系；保留 `01` 至 `09` 完整章节，每章仅含简短摘要和子文档链接。
- `prd-01-product-vision-and-goals.md`：产品愿景、本期目标与成功定义。
- `prd-02-users-and-journeys.md`：目标用户与 JTBD；带稳定 ID（`UJ-{id}`）的用户旅程；进入条件、主流程、价值结果、关键分支与异常流程。
- `prd-03-scope-and-capabilities.md`：MVP 范围、非目标、延期项；产品能力架构图；模块职责、关系与外部能力边界。
- `prd-04-functional-requirements.md`：按产品能力分组的功能需求；稳定编号及用户旅程关联（`FR-{id} → UJ-{id}`）；角色、触发条件、行为规则与可测试结果。
- `prd-05-conceptual-domain-model.md`：核心术语和业务实体定义、概念实体关系图、实体职责与生命周期、关键业务事件，以及产品能力、用户旅程和 FR 到实体的映射；不描述数据库表、字段、存储或技术实现。
- `prd-06-business-and-data-rules.md`：业务、状态、数据、权限规则以及外部依赖与约束；引用概念领域模型中的实体，不重复定义实体关系。
- `prd-07-non-functional-requirements.md`：性能、安全与隐私、可靠性与可用性、兼容性与可访问性的量化要求。
- `prd-08-metrics-and-experiments.md`：核心指标、目标值、测量方式与反向指标。
- `prd-09-decisions-and-open-questions.md`：决策与变更记录、假设、开放问题及其关闭状态。

**概念与技术实现边界**

`prd-05-conceptual-domain-model.md` 回答“业务中有哪些对象、它们如何关联、何时变化”；`arch-03-data-architecture.md` 回答“这些对象如何被技术系统实现和存储”。前者使用业务语言，不包含表名、字段类型、索引、数据库选型或接口实现；后者必须引用前者的实体定义，不得静默改变其业务含义。

**验收标准**

- [ ] `prd-00-index.md` 保留全部子章节；每章仅包含 1–3 句摘要和到对应子文档的相对链接；
- [ ] 与Product Brief的目标一致，所有重大变化都有决策记录；
- [ ] 目标用户、关键场景、主流程、异常流程和产品边界明确；
- [ ] 每条用户旅程具有稳定ID、进入条件、价值结果和异常路径；
- [ ] MVP范围与非目标明确，不依赖口头补充；
- [ ] 核心业务实体、关系、生命周期和关键业务事件已在概念领域模型中明确，且未混入数据库或技术实现；
- [ ] 功能需求具有稳定编号，并包含角色、条件、行为和可测试结果；
- [ ] 性能、安全、可靠性等非功能需求使用可测量阈值；
- [ ] 业务规则、权限、数据、外部依赖和约束没有关键遗漏；
- [ ] 产品能力架构只描述业务能力、模块职责和产品边界，不包含技术组件；
- [ ] 成功指标能够验证产品目标，而不只是统计使用量；
- [ ] 所有阻塞性开放问题已经关闭；
- [ ] 已完成一致性检查，确认可以进入UX/UI设计。

### `ux-ui/`

**作用**

UX/UI设计文档集继承PRD中的用户旅程，并将其转化为可理解、可操作、可实现的产品体验。PRD是用户旅程目标和范围的权威来源；UX/UI负责细化交互，不得静默改变旅程定义。为避免设计说明、流程和页面资产混成单一长文档，`ux-ui/ux-00-index.md` 是唯一入口、版本索引和 PRD 旅程映射。

**必须包含**

- `ux-00-index.md`：文档信息、版本索引、PRD 用户旅程 ID（`UJ-{id}`）映射、设计交付物索引与追踪关系；保留 `01` 至 `07` 完整章节，每章仅含简短摘要和子文档链接。
- `ux-01-design-goals-and-foundations.md`：设计目标、体验原则、目标用户、关键场景、平台与设备范围。
- `ux-02-information-architecture.md`：内容层级、导航结构、页面地图与术语规范。
- `ux-03-user-flows.md`：核心任务路径、关键分支、异常与恢复流程；每条流程引用相应 `UJ-{id}`。
- `ux-04-pages-and-wireframes.md`：关键页面目标、内容与操作区域、线框图、页面跳转关系；具体图稿放入 `assets/` 并由稳定页面 ID 引用。
- `ux-05-interaction-and-states.md`：默认、加载、成功、失败、空和边界状态，以及权限与角色差异。
- `ux-06-visual-design-and-components.md`：视觉方向、高保真页面、响应式适配、设计变量、通用组件、组件状态和使用规则。
- `ux-07-accessibility-and-validation.md`：可用性与可访问性要求、设计验收方法、已知缺口与交付结论。

**验收标准**

- [ ] `ux-00-index.md` 保留全部子章节；每章仅包含 1–3 句摘要和到对应子文档的相对链接；
- [ ] 设计目标、用户、场景和平台范围与PRD一致；
- [ ] PRD中的所有核心用户旅程都有对应的UX/UI方案；
- [ ] UX/UI使用PRD中的原始用户旅程ID，且未静默改变旅程目标、范围或结果；
- [ ] 信息架构、导航结构和页面层级清楚且术语一致；
- [ ] 核心流程、关键分支、异常和恢复路径均有流程图；
- [ ] 每个关键页面都有线框图，并明确页面目标、内容、操作和跳转关系；
- [ ] 高保真设计覆盖核心页面及默认、加载、成功、失败、空状态和权限差异；
- [ ] 通用组件、设计变量、组件状态和使用规则可被开发复用；
- [ ] 响应式、多端适配、可用性和可访问性要求明确；
- [ ] 设计稿、流程、页面、组件和PRD需求之间可以相互追踪；
- [ ] 不存在阻塞架构设计、Story拆分或前端实现的设计缺口。

### `architecture/`

**作用**

系统架构文档集把PRD中的产品能力转化为统一、可执行的技术约束，重点防止不同开发者或开发代理采用互相冲突的实现方式。为避免上下文、接口、运行治理和架构决策彼此混杂，`architecture/arch-00-index.md` 是唯一入口、版本索引和需求到架构映射入口。

**必须包含**

- `arch-00-index.md`：文档信息、版本索引、产品能力/FR/NFR 到组件和架构决策的映射；保留 `01` 至 `08` 完整章节，每章仅含简短摘要和子文档链接。
- `arch-01-system-context-and-principles.md`：系统上下文图、外部参与者和系统、职责与非职责、架构范式、分层与依赖方向、架构约束。
- `arch-02-components-and-code-mapping.md`：组件架构图、职责、交互关系与代码目录映射。
- `arch-03-data-architecture.md`：以 `prd-05-conceptual-domain-model.md` 为输入的逻辑/物理数据模型、技术实体关系图、数据流、存储与一致性、数据生命周期；不得静默改变概念实体的业务含义。
- `arch-04-interfaces-and-integrations.md`：内部接口、外部 API 与事件、错误处理、重试与兼容策略。
- `arch-05-security-and-operations.md`：认证与权限、安全、隐私、审计、日志、配置、错误处理、性能、可靠性、可观测性、备份与恢复。
- `arch-06-deployment-and-scalability.md`：环境与部署架构图、基础设施、第三方服务、配置与密钥管理、技术栈及版本；容量与增长假设、可独立扩展的组件及瓶颈、横向/纵向扩展策略、缓存/队列/异步处理、数据扩展、限流与降级、扩容触发条件、压测与成本约束。
- `arch-07-architecture-decisions.md`：稳定编号（`AD-{id}`）的架构决策、状态、适用范围、Binds、Prevents 与可验证 Rule。
- `arch-08-open-questions-and-deferred-decisions.md`：延期决策、原因、责任人、触发条件与开放问题。

**验收标准**

- [ ] `arch-00-index.md` 保留全部子章节；每章仅包含 1–3 句摘要和到对应子文档的相对链接；
- [ ] 系统边界、组件职责、依赖方向和外部系统清楚；
- [ ] 每项核心功能、UX关键流程及非功能需求均映射到组件或架构决策；
- [ ] 数据模型、接口契约、状态、错误和一致性策略明确；
- [ ] 身份、权限、安全、隐私和审计要求有对应方案；
- [ ] 性能、可靠性、可观测性、部署、备份和恢复方案可执行；
- [ ] 容量假设、扩展边界、扩容/降级策略、触发阈值和验证方法明确，并能追溯到适用的非功能需求；
- [ ] 关键技术栈及版本已确认与现有环境兼容；
- [ ] 关键架构决策具备稳定编号、适用范围和可执行约束；
- [ ] 每项架构决策均明确Binds、Prevents和Rule，且规则可以被代码或评审验证；
- [ ] 延期决策明确记录原因、责任人和触发条件；
- [ ] 不存在阻塞Story拆分的架构问题。

### `epics-and-stories.md`

**作用**

Epic与Story文档把PRD拆成可排序、可追踪、可实施的工作单元，同时保留需求覆盖关系和整体交付顺序。

**必须包含**

```text
1. 文档信息
2. 需求清单
   2.1 功能需求清单
   2.2 非功能需求清单
   2.3 用户旅程与UX/UI设计引用
3. Epic总览
   3.1 Epic清单
   3.2 交付价值与范围
   3.3 依赖与建议顺序
4. Epic定义
   4.1 Epic目标与业务价值
   4.2 包含范围与完成条件
   4.3 关联需求
5. Story清单
   5.1 Story编号与名称
   5.2 Story价值与范围
   5.3 FR、NFR与用户旅程引用
   5.4 UX/UI页面与状态引用
   5.5 验收条件摘要
   5.6 依赖与架构决策引用
6. 需求覆盖矩阵
   6.1 FR与NFR到Story映射
   6.2 用户旅程与UX/UI到Story映射
   6.3 架构决策到Story映射
7. 实施顺序与依赖
8. 风险与开放问题
```

**验收标准**

- [ ] 每项FR和适用的NFR都被至少一个Story覆盖，覆盖率为100%；
- [ ] Epic按用户或业务价值组织，而不是只按技术层划分；
- [ ] 每个Story可独立实施，并产生可验证结果；
- [ ] 每个Story具有需求来源、明确范围和可测试验收条件；
- [ ] 每条用户旅程及UX/UI中的关键页面、交互状态和异常流程已落实到对应Story；
- [ ] Story引用其必须遵守的架构决策，覆盖矩阵不存在孤立项；
- [ ] Story只依赖已经完成或排在前面的工作，不存在前向依赖；
- [ ] 数据、接口和基础设施在首次实际需要它们的Story中建设；
- [ ] Story顺序符合业务流程、架构约束和依赖关系；
- [ ] 不存在需求遗漏、重复Story、冲突或空占位符；
- [ ] 拆分结果已经具备进入就绪检查的条件。

### `implementation-readiness.md`

**作用**

实施就绪报告不是新的设计文档，而是对PRD、UX/UI、架构和Epic/Story进行交叉检查，判断项目是否可以安全进入开发。

**必须包含**

```text
1. 检查信息
   1.1 检查范围与日期
   1.2 输入文档及版本
2. 结论摘要
   2.1 就绪状态
   2.2 关键结论
3. PRD检查
4. 架构检查
5. 需求覆盖检查
6. Epic与Story质量检查
7. UX/UI一致性检查
8. 问题清单
   8.1 阻塞问题
   8.2 高、中、低级问题
   8.3 整改动作与责任人
9. 风险接受记录
10. 下一步行动
```

**验收标准**

- [ ] 明确列出本次检查使用的PRD、UX/UI、架构和Epic/Story版本；
- [ ] 逐项验证需求覆盖、架构承载和Story验收条件；
- [ ] 跨文档的范围、术语、用户流程、依赖和技术约束保持一致；
- [ ] 所有发现按阻塞、高、中、低分级，并有证据和整改责任人；
- [ ] 所有阻塞问题已经关闭，或留有正式的风险接受记录；
- [ ] 报告结论明确为`READY`。

### `sprint-status.yaml`

**作用**

Sprint Status是开发阶段的执行索引，用于持续记录Epic、Story和回顾项的顺序及状态。它不重复Story内容。

**必须包含**

```yaml
generated: YYYY-MM-DDTHH:mm:ssZ
last_updated: YYYY-MM-DDTHH:mm:ssZ
project: project-name
project_key: project-key
tracking_system: file-system
story_location: docs/development/stories

development_status:
  epic-1: backlog
  1-1-story-name: backlog
  1-2-story-name: ready-for-dev
  epic-1-retrospective: optional

action_items:
  - epic: 1
    action: action-description
    owner: owner-name
    status: open
```

状态枚举：

- Epic：`backlog`、`in-progress`、`done`；
- Story：`backlog`、`ready-for-dev`、`in-progress`、`review`、`done`；
- Retrospective：`optional`、`done`；
- Action Item：`open`、`in-progress`、`done`。

**验收标准**

- [ ] `generated`、`last_updated`、`project`、`project_key`、`tracking_system`和`story_location`字段完整有效；
- [ ] 所有Epic和Story均已登记，数量、编号、名称和顺序与源文档一致；
- [ ] 每个Epic都包含对应的Story和回顾项；
- [ ] 不存在源文档之外的孤立任务；
- [ ] 所有条目使用约定的合法状态，并遵守状态转换规则；
- [ ] 已有`action_items`在更新时完整保留，状态和值未被意外覆盖；
- [ ] 只有已经就绪的Story可以进入开发状态；
- [ ] 文件能够持续更新并准确反映当前开发进度。

### `stories/story-{id}.md`

**作用**

Story文档是单个开发任务的完整实施上下文，应让开发者无需重新推断需求、架构或验收方式即可开始实现。

**必须包含**

```text
1. Story信息
   1.1 Story编号与名称
   1.2 所属Epic与状态
   1.3 来源文档
2. 用户价值
3. 范围与非范围
4. 来源与依赖
   4.1 PRD需求
   4.2 架构决策与UX设计
   4.3 前置Story与相关代码
5. 验收条件
   5.1 主流程
   5.2 异常与权限
   5.3 关键边界情况
6. 开发任务
   6.1 任务与子任务
   6.2 任务到验收条件映射
7. 技术说明
   7.1 复用点与文件位置
   7.2 接口与数据结构
   7.3 技术约束与禁止做法
8. 测试要求
9. 开发前完成定义
10. 实施记录（开发完成后填写）
    10.1 实际改动文件
    10.2 技术偏差与测试结果
    10.3 遗留问题
11. 代码评审与完成结论（开发完成后填写）
```

**开发前验收（`ready-for-dev`）**

- [ ] 标明Story编号、所属Epic、业务价值、范围和非范围；
- [ ] 引用对应的PRD需求、用户旅程、UX/UI设计、架构决策和前置Story；
- [ ] 验收条件覆盖主流程、异常、权限和关键边界情况；
- [ ] 每条验收条件都能通过测试或可观察结果判定；
- [ ] 开发任务完整，并能对应到具体验收条件；
- [ ] 明确复用点、文件位置、接口、数据结构和技术约束；
- [ ] 测试要求覆盖该Story实际需要的单元、集成、接口或端到端测试；
- [ ] 所有依赖已满足，且不存在模板占位符或阻塞性未决问题；
- [ ] Story验证结果为`ready-for-dev`。

> `ready-for-dev`验收不要求填写实施记录、实际改动文件或测试结果；这些内容在开发过程中补充。

**开发完成验收（`done`）**

- [ ] 所有开发任务和验收条件均已完成；
- [ ] 必需的单元、集成、接口或端到端测试全部通过；
- [ ] 实际改动文件、测试结果和技术偏差已完整记录；
- [ ] 实现遵守PRD、UX/UI和架构约束，任何偏差均有明确说明；
- [ ] 遗留问题已关闭，或已形成有边界、有后续处理条件的记录；
- [ ] 代码评审不存在阻塞问题；
- [ ] Story状态已更新为`done`。

## 工具使用

### BMad 的角色与边界

BMad Method 用于帮助团队按步骤完成调研、产品定义、PRD、设计、架构、Story 和实施就绪检查。它可以生成结构化草稿、提出遗漏问题、维护流程上下文，但**不能替代本规范的阶段门禁、事实核验、产品决策、人工审批或最终责任**。

使用 BMad 前，先确认项目已完成安装并能在 Codex 中调用 `bmad-help`。安装与基础使用参见 [新手开发环境准备指南](新手开发环境准备指南.md)。

### 统一工作方式

1. **先定位阶段**：打开本 GUIDE，明确当前要交付的文档和通过证据；不要直接要求 AI“做完整产品”。
2. **先读取上游**：将已通过的上游文档、现有 `*-00-index.md`、相关来源和明确约束提供给 BMad。
3. **先问下一步**：在 Codex 的新任务中输入 `bmad-help`，说明当前阶段、已有文件和目标，让它列出当前已安装工作流中最合适的下一步。
4. **一次完成一个工作流**：完成一个工作流后，新开任务或对话，再开始下一项工作，避免上下文混杂。
5. **按本规范落盘**：将输出整理到本 GUIDE 规定的目录和文件名中；不得只保留聊天记录或 BMad 原始输出。
6. **人工验收后再推进**：逐项执行本 GUIDE 对应文档的验收标准；未通过时，回到 BMad 补充或修订，而不是跳过门禁。

> **推荐提示词**：`bmad-help 当前项目要完成 <文档名称>。已有输入是 <文件路径/链接>。请只推荐下一步可用的工作流、所需输入、预期产出和需要人工确认的事项。`

### BMad 与文档阶段的对应方式

| 阶段与交付物 | 让 BMad 协助完成的工作 | 人工必须确认的事项 |
|---|---|---|
| `product-brief.md` | 梳理问题假设、目标用户、场景、价值主张、范围与试点指标；提出证据缺口。 | 事实来源、问题真实性、首版边界、指标目标值和继续投入结论。 |
| `prd/` | 从已通过的 Brief 生成用户旅程、能力、FR、概念领域模型、业务规则、NFR、指标与开放问题的草稿。 | `UJ-*`、`FR-*` 的稳定性；实体关系是否保持业务语言；需求是否可测试；范围、权限与外部约束是否完整。 |
| `ux-ui/` | 将用户旅程细化为信息架构、流程、页面、状态、组件和验收建议。 | 不得静默改写 PRD 旅程；关键流程、异常、权限和可访问性是否覆盖。 |
| `architecture/` | 提出系统边界、组件、数据、接口、质量属性与架构决策候选。 | 技术选型、接口契约、安全、成本、可用性与每个 `AD-*` 决策的可执行约束。 |
| `epics-and-stories.md` 与 Story | 按价值、依赖和验收条件拆分 Epic/Story，并生成覆盖矩阵草稿。 | 需求覆盖率、无前向依赖、开发顺序与每条 Story 的可测试性。 |
| `implementation-readiness.md` | 对 PRD、UX/UI、架构和 Story 做一致性检查，列出缺口、冲突与风险。 | 阻塞项是否真实关闭，以及最终 `READY` 结论。 |

### 按目录构建文档集

对 `prd/`、`ux-ui/` 和 `architecture/`，不要让 BMad 一次生成一篇大文档。按以下节奏工作：

1. 先用 BMad 生成 `*-00-index.md` 的目录、每章 1–3 句摘要和子文档链接；
2. 再按 `01`、`02` 的顺序逐个生成子文档草稿；
3. 每次生成后补齐稳定 ID、来源、决策和相对链接；
4. 回到 `*-00-index.md`，确认所有章节、摘要与链接完整且不重复细节；
5. 最后让 BMad 做跨文档检查，再由责任人按验收标准签字或记录待整改项。

> **禁止做法**：不要把 BMad 自动生成的目录、编号、指标、用户事实或技术结论直接视为已确认事实；不要因为 BMad 能继续下一步，就跳过上游文档的验收。

### 可直接复制的提示词模板

#### 生成单个子文档草稿

```text
请基于以下已通过的输入，为 <prd/ux-ui/architecture> 的 <编号与文件名> 生成草稿。

必须遵守 docs/GUIDE.md 中该文件的职责、必须内容和验收标准；
引用已有稳定 ID，不新建或改写未获批准的 ID；
不确定的信息标记为“待确认”，不要补写为事实；
输出前列出：使用的来源、仍缺失的输入、需要人工决策的事项。
```

#### 检查文档集是否可进入下一阶段

```text
请检查 <当前文档集路径> 是否满足 docs/GUIDE.md 中 <阶段名称> 的验收标准。

逐项输出：通过 / 待整改 / 不通过、对应证据位置、缺口、建议修复动作和责任角色。
不要将未验证的 BMad 输出当作通过证据；不要替我作最终放行结论。
```

### 出现问题时怎么办

- **不知道调用哪个 BMad 工作流**：先使用 `bmad-help`，让它根据已安装模块和项目状态推荐，不要猜测技能名称。
- **输出与 GUIDE 结构不一致**：以 GUIDE 为准；让 BMad 按指定文件、章节、稳定 ID 和验收条件重写。
- **资料不足**：停止扩写，把缺口放入开放问题，并明确需要谁补充什么来源或决策。
- **BMad 生成内容过长**：拆成单个子文档；`00-index` 只留摘要和链接，详细内容留在子文档。

## 判定原则

- **通过**：全部门禁条件满足，无阻塞问题，可以进入下一阶段。
- **待整改**：存在明确缺口，完成整改并复核后才能通过。
- **不通过**：目标、范围、方案或验收条件存在根本缺失，必须返回上游阶段修正。
- “风险已知”不等于“风险已解决”；只有责任人、处理期限和正式接受记录齐全时，风险才能不阻塞放行。
- 下游文档不得静默修改上游决定。需求变化必须先更新PRD，再同步架构、Story和Sprint状态。

> 本规范将UX/UI作为开发前的必需设计基线。纯API、CLI或无用户界面的项目可以将该文档标记为不适用，但必须在实施就绪报告中说明理由。
