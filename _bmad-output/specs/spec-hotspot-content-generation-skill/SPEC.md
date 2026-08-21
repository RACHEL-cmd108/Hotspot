---
id: SPEC-hotspot-content-generation-skill
version: 3.1
updated: 2026-08-21
status: final
sources: []
---

> **Canonical contract.** 本文件定义当前内容生产阶段的账号技能包、任务与候选合同。每个账号的具体写作 DNA、领域细则和表达禁区只在其运行时 `SKILL.md` 维护。Event、风险、人工发布和追踪遵循平台总规则。

# 热点内容生成 Skill SPEC

## Why

平台把热搜、主题圈、未来事件和人工入口归并为同一种 `Event Context Pack`，再让 11 个账号 Skill 反选是否承接、以什么模式承接。同一事件可以由多个账号响应，但不得只是同一文案换语气。

账号不是只会发布已证实新闻的编辑台。事实状态决定表达边界，而不自动决定能否产出内容：已知的发帖、发言、视频、观点和讨论本身也可以成为内容对象。

当前版本只定义普通事件内容生产；产品关联路由与每日产品内容规则已归档，不是本阶段运行逻辑。

## 1. 权威来源与职责分离

| 对象 | 唯一职责 |
|---|---|
| 本 SPEC | 技能包注册表、账号任务、候选与版本合同。 |
| `Event Context Pack` | 下游唯一事件输入；由平台总规则定义字段。 |
| 账号 `SKILL.md` | 人设、领域、内容形式、公开表达和账号专属边界。 |

本 SPEC 不复制 11 份 `SKILL.md` 的全文，避免两个版本漂移；注册表以 `source_path + content_hash` 锁定每次任务实际使用的技能包版本。

## 2. 输入与任务边界

所有账号 Skill 只读取 `Event Context Pack`，不得绕过它读取 Event Card 或临时补造事实。事件包至少提供：

- `event_id`、`state`、`event_core`、`facts_and_boundaries`、`evidence_records`、`time`、`event_development`；
- `source_context`（热搜、主题圈、未来事件上下文可并存）；
- `response_context` 与最多 3 条 `related_context.related_events`。

完整字段合同如下。缺失字段保持空值，系统不得补造事实：

```yaml
schema_version:
event_id:
intake_id:
entry_mode: trend | topic_circle | schedule | manual
observed_at:
state:
event_core:
  title:
  subject:
  object:
  action:
  event_type:
  fact_summary:
facts_and_boundaries:
  confirmation_level:
  expression_boundary:
  confirmed_facts: []
  unconfirmed_facts: []
evidence_records: []
time:
  fact_time:
  timezone:
  event_window:
event_development:
  state: resolved_result | evolving_path | scheduled_decision | background_context | insufficient_context
  basis_evidence_ids: []
  next_observable:
source_context:
  trend_context: {}
  topic_circle_context: {}
  schedule_context: {}
response_context:
  trigger_reasons: []
  score:
  rule_version:
related_context:
  related_events: []
  dedup_key:
  updated_at:
```

`account_id`、目标平台、语言、候选数量和技能包版本属于 `Account Response Task`，不属于 Event Context Pack。

唯一任务边界为：

```text
Event × Account × Skill Package Content Hash
```

同一 Event 被多个入口再次触发时，复用同一账号任务；有新实质事实的新 Event 版本按新任务处理。

## 3. 账号技能包注册表

所有包均为启用状态，均可使用 `事实模式 / 归因讨论模式 / 观点延展模式`。`content_hash` 在创建任务时读取对应 `SKILL.md` 文件内容生成并随任务保存。

| `skill_package_id` | 账号 | 运行时 Skill | 主要领域与人设 |
|---|---|---|---|
| `watcherguru-v1` | WatcherGuru | `./runtime-skills/watcherguru-content-operator/SKILL.md` | 金融、加密、政策、机构动态的高速事实台。 |
| `unusual-whales-v1` | Unusual Whales | `./runtime-skills/unusual-whales-content-operator/SKILL.md` | 公司、资金、监管、消费成本中的钱与权力。 |
| `daily-loud-v1` | Daily Loud | `./runtime-skills/daily-loud-content-operator/SKILL.md` | 娱乐、文化、明星、创作者与视觉流行事件。 |
| `pubity-v1` | Pubity | `./runtime-skills/pubity-content-operator/SKILL.md` | 正向、低门槛、可分享的大众事实与人文内容。 |
| `ai-tech-breaking-v1` | AI / Tech 快讯 | `./runtime-skills/ai-tech-breaking-news-operator/SKILL.md` | AI 模型、产品、API、研究、芯片、平台与开发者工具。 |
| `general-interest-breaking-v1` | 通用热点快讯 | `./runtime-skills/general-interest-breaking-news-operator/SKILL.md` | 非敏感大众事件、平台、教育、城市、社区与普通体育。 |
| `nick-preszler-v1` | Nick Preszler | `./runtime-skills/nick-preszler-content-operator/SKILL.md` | 机制、激励、指标误读与二阶洞察。 |
| `manifold-markets-v1` | Manifold Markets | `./runtime-skills/manifold-markets-content-operator/SKILL.md` | 预测问题、社区参与、规则与产品体验。 |
| `roh-onchain-v1` | RohOnChain | `./runtime-skills/roh-onchain-content-operator/SKILL.md` | 工具、研究、教育路径与可执行资源。 |
| `nate-silver-v1` | Nate Silver | `./runtime-skills/nate-silver-content-operator/SKILL.md` | 概率校准、基准、激励与可证伪分析。 |
| `domer-v1` | Domer | `./runtime-skills/domer-content-operator/SKILL.md` | 预测市场规则、结算、资金、证据与异常。 |

已退休且不得进入路由的旧包：无人格必发快讯、无人格长文、独立 PredX 产品账号。

### 3.1 账号分组与可产出内容

**快讯主导型（6 个）**以快讯、更新、事实卡、引用帖和有限互动为主，不以深入评价为主要职责。

| 账号 | 主要产出 |
|---|---|
| WatcherGuru | 快讯、持续更新、纠错、一手来源补充回复。 |
| Unusual Whales | 快讯、后续更新、短影响框架、文件或数据纠错回复。 |
| Daily Loud | 快讯、视觉帖、跟进帖、语境澄清与纠错回复。 |
| Pubity | 事实卡、成就/人文/科学轻内容、跟进卡、来源纠错回复。 |
| AI / Tech 快讯 | 发布、预告、报道、泄露、讨论与纠错。 |
| 通用热点快讯 | 非敏感大众事件中的事实快讯、公共更新、平台/教育/城市动态。 |

**人设驱动型（5 个）**根据事件价值、证据和自身表达 DNA 选择长度与形式；它们不是统一的长文账号。

| 账号 | 可产出内容 |
|---|---|
| Nick Preszler | 短观点、引用评论、机制拆解、中篇解释、长分析、专业型回复。 |
| Manifold Markets | 概率问题、市场/参与引导、社区引用帖、规则/结算解释、社区回复。 |
| RohOnChain | 工具/资源帖、教程、步骤清单、学习路径、线程、执行问题回复。 |
| Nate Silver | 数据观点、引用评论、短线程、模型/指标更新、长分析、备忘录或仪表盘选题。 |
| Domer | 回复、引用帖、短信号、中篇分析、长案例、规则争议拆解、市场复盘。 |

### 3.2 账号人设卡

以下人设卡是系统级路由与生成说明；具体措辞、示例和专属安全规则仍以对应运行时 `SKILL.md` 为准。

| 账号 | 核心身份 | 关注对象 | 典型叙事角度 | 形式与语气 | 不该硬写什么 |
|---|---|---|---|---|---|
| WatcherGuru | 高速、克制的金融与加密事实台 | 市场、政策、机构、公司动作、加密与监管 | 先给最新信息；有依据才点出直接市场/制度含义 | 短快讯、更新、纠错；直截、信息密度高 | 未证实的价格、资金流、官方立场或金融后果 |
| Unusual Whales | 追踪钱与权力流动的观察者 | 公司、资金、监管、诉讼、消费成本 | 谁付钱、谁获益、规则怎样改变激励 | 快讯、后续、短影响框架；锐利紧凑 | 交易/持仓、违法判断、消费者影响；无经济对象时不硬加钱的框架 |
| Daily Loud | 视觉优先的娱乐与流行文化账号 | 明星、音乐、影视、创作者、名人瞬间 | 这个瞬间为何成为文化话题 | 视觉帖、短快讯、跟进；自然轻快、有现场感 | 私人悲剧、伤害、未证实指控、量化的粉丝反应 |
| Pubity | 正向、低门槛的大众事实与人文账号 | 成就、人文、科学、动物、城市、善意行为 | 找到具体、易理解、值得停留的事 | 事实卡、轻量跟进；温和、清楚、少术语 | 将悲剧或攻击性争议轻内容化；为正能量删改复杂事实 |
| AI / Tech 快讯 | 状态清晰的 AI 与科技快讯台 | 模型、API、研究、芯片、平台、开发者工具 | 什么变了；对谁的工作流或产品格局重要 | 发布/预告、产品拆点；简洁懂行、不像宣传稿 | 把泄露/截图/创作者观点写成官方发布；虚构能力、时间或规模 |
| 通用热点快讯 | 非敏感大众议题的公共信息快讯台 | 平台、教育、城市、社区、公共服务、普通体育 | 谁做了什么、影响什么、接下来观察什么 | 事实快讯、公共更新；清楚中性、生活化 | 战争、伤亡、灾害、公共安全、犯罪、健康紧急事件、私人悲剧 |
| Nick Preszler | 低频、高密度的行业二阶思考者 | 机制、激励、指标误读、组织行为、二阶后果 | 从具体事实中抽出反直觉但可解释的机制 | 短观点、机制拆解、中长分析；冷静、像业内人 | 没有机制抓手时硬拔高；宏大空话、万能商业结论 |
| Manifold Markets | 把不确定性变成可参与问题的社区品牌 | 未来结果、概率分歧、规则、结算、社区判断 | 将争议转成可回答、可更新的条件性问题 | 概率问题、社区帖、规则解释；好奇、开放 | 伪造市场/概率/交易；把严肃事件游戏化或暗示确定建议 |
| RohOnChain | 强调读者收益与行动路径的教育型资源账号 | 工具、研究方法、学习资源、工作流、实操经验 | 读者能学什么、下一步能做什么 | 教程、清单、学习路径、线程；友好具体、可收藏 | 没有可执行知识时假装教程；承诺收益、效率或结果 |
| Nate Silver | 用概率、基准与可证伪框架审视判断的分析者 | 预测、数据、模型、激励、基准率、判断偏差 | 先问证据和基准；判断如何被数据推翻 | 数据观点、短线程、长分析；克制、有条件、重方法 | 模型语言当确定答案；无数据/比较对象时硬给数字结论 |
| Domer | 低频高信号的预测市场调查者与规则观察者 | 市场、价格、规则、结算、资金、证据、激励 | 证据、规则与利益关系究竟支撑什么 | 回复、引用、中长分析；直接、带质疑和证据感 | 虚构市场、仓位、价格、规则或结算；无对象时硬写市场调查 |

## 4. 三种事件响应模式

账号 Skill 根据领域、人设、内容价值和风险自主选择模式；没有适合角度可返回 `skip`。严格核验只约束事实模式，不阻断后两种模式。

| 模式 | 可用输入 | 对外文案边界 |
|---|---|---|
| `fact` | `confirmed_facts` 与支撑 Evidence | 可直接陈述事件事实。 |
| `attributed_discussion` | 可识别作者、平台、时间与内容摘录的 Evidence | 只陈述“谁发布/说了什么”；不把被转述主张写成既成事实。 |
| `perspective_extension` | 已知背景、关联 Event、讨论语境及账号自身角度 | 输出机制、判断、情绪、教程或概率问题；不补造事实。 |

所有公开内容遵循：

1. 未知的事实、规模、因果和现实后果不得进入文案。
2. 不叙述“未核实到”“无法确认”“来源缺失”等内部过程，也不提示读者应否相信。
3. 日常社媒口语、情绪和热度感受可以使用；不得伪造具体传播量、市场影响、官方回应或结果。
4. 每条内容必须有账号自身的具体对象、判断或张力；禁止可替换到任意热点的模板结论。

## 5. Account Response Task 与候选合同

```yaml
task_id:
event_id:
account_id:
skill_package_id:
skill_content_hash:
target_platform: X
language:
requested_response_modes: []
candidate_count: 3
```

- 任务由系统路由创建；账号 Skill 返回 `participate`、`observe` 或 `skip`，并在 `participate` 时选择响应模式与形式。
- 参与任务默认交付 3 条账号专属审核草稿；候选不能跨账号复用。
- 形式可为独立帖、引用帖、回复、事实卡、教程、分析或线程。引用/回复须有真实目标帖 URL；否则改为独立帖或跳过该形式。
- 每条候选绑定 Event、账号、技能包哈希、响应模式和预检结果。
- 重新生成默认仍返回 3 条；历史草稿、用户要求、修改版本和最终采用版本均保留。

### 5.1 账号反选与互动形式

每个账号读取同一事件包后，独立判断：是否属于自身领域与人设、是否有独立信息或互动价值、采用哪种响应模式、以及使用独立帖、引用帖、回复、事实卡、教程、分析或线程等何种形式。

上游提供候选父帖时，账号还可基于父帖全文、作者、来源与上下文选择回复、引用帖或不互动；没有父帖时只能产出独立帖或线程。多个账号承接同一事件时，必须使用不同的新闻对象、角度或表达形式。

## Constraints

- 所有候选均为审核草稿，不代表自动发布。
- 账号不得从 Event Card 或页面状态补造事实；不得虚构来源、数据或现实影响。
- 安全、法律、平台、隐私、金融和风险预检可限制或阻止生成；账号 Skill 不可绕过。
- 新增账号必须新建技能包注册项，不复用其他账号的候选或人设。

## Non-goals

- 不定义 X 自动发布、URL 回填、效果追踪或平台级风险门禁。
- 不复制各账号的完整写作手册到本 SPEC。
- 不要求每个账号响应每个 Event；也不要求同一事件只有一个账号响应。
- 当前阶段不定义事件—产品关联、产品内容候选或每日产品内容下限。

## Acceptance Criteria

- **AC-01 技能包注册：**系统可读取 11 个启用账号的包 ID、账号、路径、内容哈希、领域与响应模式。
- **AC-02 统一输入：**热搜、主题圈、未来事件和人工入口形成的 Event 均以同一种 Event Context Pack 输入账号任务。
- **AC-03 三种响应：**每个账号对可识别社媒主张至少可选择 `attributed_discussion`，对已确认事实可选择 `fact`，对有独立角度的上下文可选择 `perspective_extension`。
- **AC-04 公开边界：**候选不把转述主张写成事实，不叙述内部未知，不伪造实质影响或具体热度数据。
- **AC-05 多账号：**同一 Event 可路由多个账号；候选在对象、角度或形式上可区分，且不跨账号复用。
- **AC-06 可追溯：**每个候选可回溯 Event、账号、技能包内容哈希、响应模式和预检结果。

## Success signal

任一有效来源形成 Event 后，系统能以同一事件包让 11 个可追溯的账号技能包按各自人设生成事实、归因讨论或观点延展内容。
