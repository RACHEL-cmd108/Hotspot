# 热点内容生成 Skill

## 1. 当前模型

系统的活跃内容生产能力由 **11 个账号 Skill** 组成：6 个快讯主导型账号，以及 5 个观点、教育、社区或分析型账号。

它们都接收上游生成的统一事件上下文包，并自主判断是否以本账号的领域、人设与内容方式承接。一个事件可由多个账号承接，但每个账号必须有独立的新闻对象、角度或表达形式，不能只是同一文案换语气。

已退休的独立生产线：无人格必发快讯、无人格长文、独立 PredX 产品账号。产品相关内容不再由单独账号垄断，而是成为 11 个账号都可调用的内容能力。

## 2. 11 个账号 Skill

### 快讯主导型账号（6 个）

这些账号以快讯、更新、事实卡、引用帖和有限互动为主，不以深入评价为主要职责。

| 账号 / Skill | 领域与人设 | 主要产出 |
|---|---|---|
| [WatcherGuru](/Users/rachelyuan/.codex/skills/watcherguru-content-operator/SKILL.md) | 金融、加密、政策、机构动态的高速事实台 | 快讯、持续更新、纠错、一手来源补充回复 |
| [Unusual Whales](/Users/rachelyuan/.codex/skills/unusual-whales-content-operator/SKILL.md) | 公司、资金、监管、诉讼、消费成本中的“钱与权力”视角 | 快讯、后续更新、短影响框架、文件/数据纠错回复 |
| [Daily Loud](/Users/rachelyuan/.codex/skills/daily-loud-content-operator/SKILL.md) | 视觉优先的娱乐、文化、明星、创作者与流行事件账号 | 快讯、视觉帖、跟进帖、语境澄清与纠错回复 |
| [Pubity](/Users/rachelyuan/.codex/skills/pubity-content-operator/SKILL.md) | 正向、低门槛、可分享的大众事实账号 | 事实卡、成就/人文/科学轻内容、跟进卡、来源纠错回复 |
| [AI / Tech 快讯](/Users/rachelyuan/.codex/skills/ai-tech-breaking-news-operator/SKILL.md) | AI 模型、产品、API、研究、芯片、平台与明确标注泄露的状态清晰快讯台 | 已证实发布、官方预告、具归因报道或泄露快讯、更新与纠错 |
| [通用热点快讯](/Users/rachelyuan/.codex/skills/general-interest-breaking-news-operator/SKILL.md) | 其他非敏感大众事件、平台、教育、城市、社区与普通体育 | 事实快讯、公共更新、平台/教育/城市动态 |

### 人设驱动型账号（5 个）

这些账号根据事件价值、证据和自身表达 DNA 选择长度与形式；它们不是统一的“长文账号”。

| 账号 / Skill | 基本面与表达 DNA | 可产出内容 |
|---|---|---|
| [Nick Preszler](/Users/rachelyuan/.codex/skills/nick-preszler-content-operator/SKILL.md) | 低频行业思考者；关注机制、激励、指标误读与二阶影响 | 短观点、引用评论、机制拆解、中篇解释、长分析、专业型回复 |
| [Manifold Markets](/Users/rachelyuan/.codex/skills/manifold-markets-content-operator/SKILL.md) | 社区原生的预测市场品牌；把不确定性变成参与 | 概率问题、市场/参与引导、产品演示、社区引用帖、规则/结算解释、社区回复 |
| [RohOnChain](/Users/rachelyuan/.codex/skills/roh-onchain-content-operator/SKILL.md) | 可收藏、可执行的教育型账号；强调读者收益与行动路径 | 工具/资源帖、教程、步骤清单、学习路径、线程、执行问题回复 |
| [Nate Silver](/Users/rachelyuan/.codex/skills/nate-silver-content-operator/SKILL.md) | 概率校准、基准比较、激励分析和可证伪观点 | 数据观点、引用评论、短线程、模型/指标更新、长分析、备忘录或仪表盘选题 |
| [Domer](/Users/rachelyuan/.codex/skills/domer-content-operator/SKILL.md) | 低频高信号的预测市场调查者；关注价格、规则、资金、证据与激励 | 回复、引用帖、短信号、中篇分析、长案例、规则争议拆解、市场复盘 |

## 3. 统一事件链路

```text
热点源 + 信息源
→ 统一事件上下文包
→ 事件—产品关联检测
→ 账号 Skill 反选与内容生产
```

### 3.1 上游：统一事件上下文包

上游负责抓取、聚合和核实来源，输出事件事实与上下文，不替账号决定是否发帖、发几条、用什么形式或如何表达。`Event Context Pack` 是热搜榜、主题圈、未来事件和人工入口归并后的唯一内容输入；缺失字段保持空值，不补造事实。

其字段与平台规则 SPEC 保持一致：

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
  trend_context:
    list:
    region:
    ranking:
    ranking_change:
    trigger_reason:
    representative_posts: []
  topic_circle_context:
    circle:
    discussing_accounts: []
    trigger_metrics: {}
    related_posts: []
  schedule_context:
    fact_time:
    time_precision:
    event_window:
    action_score:
    heat_query:
    heat:

response_context:
  trigger_reasons: []
  score:
  rule_version:

related_context:
  related_events: []
  dedup_key:
  updated_at:
```

`trend_context`、`topic_circle_context`、`schedule_context` 可同时存在，但都只提供发现与热度语境，不能替代 `confirmed_facts` 和 `evidence_records`。`target_platform`、`language`、`account_id` 与 `skill_version` 不属于事件包；它们属于下游为某个账号创建的内容生成任务。

### 3.2 事件—产品关联检测

每一张已形成的事件上下文包都进行一次产品关联检测。该层只判断事实：事件是否能与 PredX 建立来源支持的关联；它不写文案，也不指定账号。

```yaml
product_association:
  status: supported | none
  association_bases: []
  event_evidence_ids: []
  rationale:
  allowed_product_fact_ids: []
  allowed_presentation: []
  prohibited_claims: []
  concrete_market_matching: disabled
  checked_at:
  reference_version:
```

- `none`：事件照常进入账号路由，但只能生成普通内容。
- `supported`：事件照常进入账号路由，并额外成为产品相关内容候选。
- 事件发展状态由 `event_development` 描述；产品关联只判断 PredX 是否存在自然、来源支持的承接面。v1 不匹配或插入具体活跃市场链接、Market ID、价格或市场反应。
- 只对事件包检测一次并复用结果；新实质事实进入事件新版本后才重新检测。

### 3.3 下游：账号反选

账号 Skill 读取同一张事件包及其 `product_association`，自行决定：

1. 这件事是否属于本账号的领域与人设；
2. 是否有独立的信息增量、内容价值或互动价值；
3. 若 `product_association.status: supported`，是否值得从本账号角度产出产品相关内容；
4. 选择独立帖、引用帖、回复、事实卡、教程、分析或线程等形式；
5. 同一事件若多个账号承接，确保各自新闻对象或角度不同。

上游提供候选父帖时也是同一原则：账号 Skill 根据父帖全文、作者、来源和上下文，选择回复、引用帖或不互动；没有父帖时产出独立帖或线程。

### 3.4 三种事件响应模式

11 个账号 Skill 均可在同一事件包中选择以下一种或多种模式；严格核验只约束事实模式，不阻断后两种内容。

| 模式 | 可陈述的对象 | 写作边界 |
|---|---|---|
| 事实模式 | `confirmed_facts` 中的事件事实 | 可直接陈述发生了什么。 |
| 归因讨论模式 | `evidence_records` 中可识别的作者、平台、时间与发帖/发言行为 | 只陈述“谁发布/说了什么”；不把被转述主张写成既成事实，也不叙述未核验过程。 |
| 观点延展模式 | 已知背景、关联事件、讨论语境与账号自身角度 | 输出具体机制、判断、情绪、教程或概率问题；不补造事实或泛化为模板结论。 |

## 4. 产品相关内容规则

事件—产品关联检测的事实口径、等级、允许主张与版本维护，统一读取[PredX 事件—产品关联参考](docs/predx-event-product-association-reference.md)。

### 4.1 职责划分

- **关联层**：证明“事件能否与 PredX 相关”。
- **账号 Skill**：决定“我是否要用本账号口吻承接，以及怎样承接”。
- **每日调度层**：保证每个账号当天至少有一条产品相关内容，不限制高价值热点的后续承接。

产品相关内容只能使用 `product_association` 或产品信息包中有来源支持的产品事实、页面链接和功能描述；不得为露出而创造事件关联、市场、价格、能力或结果。v1 不使用具体活跃市场链接。

### 4.2 每日下限，无上限

每个账号每天至少产出 1 条产品相关内容；这是一条下限，而不是限额。

```yaml
account_id:
date:
product_content_count_today: 0
daily_product_minimum: unmet | met
recent_product_fact_ids: []
recent_angles: []
```

- 产品关联热点被账号承接后，`product_content_count_today` 增加，最低要求达到即标为 `met`。
- 当天后续出现更高契合度的产品关联热点，账号仍可继续承接；不设置每日产品内容上限。
- 同一事件可以由多个账号产出产品相关内容，但各账号的角度必须不同。

### 4.3 日终产品素材补位

日终检查中，只有 `product_content_count_today: 0` 的账号进入补位流程。系统从已验证的产品素材库生成一份独立的产品信息上下文包；它不伪装成热点事件。

```yaml
context_origin: product_library
product_fact_ids: []
product_sources: []
allowed_claims: []
product_page_urls: []
visual_assets: []
recent_angles: []
content_goal: daily_product_fallback
```

账号按人设生成产品内容：Roh 可写教程，Domer 可写市场案例，Nate 可写数据/概率视角，Manifold 可写参与问题，快讯账号可写与自身领域匹配的短产品更新或事实帖。

产品素材库保存的是可验证的事实材料，而不是固定广告文案：功能/更新、真实市场案例、页面与链接、使用路径、公开数据、素材与已批准的产品主张。

## 5. 共通边界

- 账号反选决定是否承接事件；上游不替账号指定文案或人设角度。
- **事件响应原则**：账号可基于已证实事实、具名报道、传闻、创作者观点或讨论热点产出内容；事实状态决定表达边界，而不是“一律能不能发”的门槛。已证实事实可直接陈述；报道须归因给报道方；传闻和转述只能陈述已知的传播与归因事实（如“一个被归因于某人的视频正在流传”），不得把转述内容写成既成事实；创作者观点与讨论热点须明确其为观点或讨论，不得伪装成客观事实或官方动态。
- **只说已知内容**：对外内容不得叙述“未核实到”“无法确认”“来源缺失”等内部认知过程，也不对读者作“应否相信”的提示。未知的事实、规模、因果和后果不进入文案；需要保留边界时，改用事实性的归因句法。非实质性的社媒口语、情绪和热度感受可以保留，只要不伪造具体传播量、市场影响、官方反应或结果。
- 因此，账号是否承接由领域、人设、内容价值和风险共同决定；不得仅因材料未获官方确认而自动跳过。安全、法律、平台规范、隐私和账号自身的明确禁区仍可阻止生成或发布。
- **账号原生表达**：事实边界必须保留，但不能把“核验说明 + 抽象观点 + 正确结论”写成固定模板。每条内容先找到该账号会真实在意的具体对象、张力或判断，再用自然语言嵌入必要归因；避免空泛三段论、机械转折、合规腔前言和可替换到任何热点上的结尾。
- 产品关联为 `none` 时，仍允许普通内容，但不允许产品硬蹭。
- 内容一律先输出为审核草稿，不代表自动发布。
- 事实、报道、泄露、推断、观点和概率必须按各账号 Skill 的证据规则清晰区分。
- 伤亡、灾害、事故、公共安全、犯罪细节、健康紧急事件与私人悲剧不进入通用热点快讯；其他账号也遵循其自身的安全与证据边界。
- 需维护近期已用的产品事实与角度，避免同一卖点在多个账号或连续日期中重复出现。

## 6. 非活跃旧 Skill

下列文件可保留作历史参考，但不再属于当前 11 个账号的生产与路由模型：

- `respond-with-breaking-brief`：无人格、必发式快讯生产线。
- `develop-hotspot-deep-dive`：无人格长文生产线。
- `bridge-hotspot-to-product`：独立 PredX 产品账号生产线；其有效产品事实与合规边界迁移为共享能力。
