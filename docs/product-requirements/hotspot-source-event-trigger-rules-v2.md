# 三类热点源与 Event 触发规则 v2

> 状态：业务规则已收口，可供产品、原型和开发实现使用
> 日期：2026-08-25
> 范围：X 热搜榜、X 关注圈层、未来事件进入统一 Event 层的触发与聚合

## 1. 与上一版的差异

### 1.1 新增

- 将热点源统一为三条独立路径：X 热搜榜、关注圈层、未来事件。
- 三条路径均可独立创建 Event，也可聚合到同一 Event。
- 热搜词先做七大类语义识别，不再只匹配固定关键词。
- 关注圈层从 50 个账号扩充到 59 个；AI 与科技圈从 10 个扩充到 19 个。
- 为 59 个账号逐一配置来源角色、单点权限和权威范围。
- 增加第一方重大事件、核心人物明确行动、帖子流量异常三类单点触发。
- 增加圈内共振与全池跨圈扩散规则。
- Event Card 增加来源标签和客观触发标签；多来源命中增加关注权重。

### 1.2 调整

- X 热搜榜从每 1 小时调整为每 2 小时抓取。
- 关注圈层从每 3 小时调整为每 2 小时抓取。
- 圈内短期统计窗口从滚动 3 小时调整为滚动 2 小时。
- 未来事件从 75/90 双门槛调整为 Action Score 达到 80 分进入 Event 匹配。
- `@crypto` 修正为 Crypto.com 官方账号 `@cryptocom`。

### 1.3 删除

- 删除“只有固定重点关键词才直接调查”的逻辑。
- 删除关注账号完全平权、没有来源角色和权威范围的配置方式。
- 删除 Future Event 的 75 分待响应、90 分自动响应双门槛。
- 删除热度高、中、低等级；只保留客观标签和内部关注权重。
- AI 与科技圈删除 `@huggingface`、`@AndrewYNg`、`@karpathy`、`@verge`、`@WIRED`。
- 不监控 `@ChatGPTapp` 和 `@JensenHuang`。

## 2. 统一对象与主流程

### 2.1 对象

- **Signal**：热点源产生的一条原始变化，例如趋势词、监控账号帖子或 Future Event 评分变化。
- **Candidate Cluster**：尚未达到 Event 门槛，但语义上可能指向同一事件的一组 Signal。
- **Event**：命中某个热点源触发规则后创建或复用的统一事件对象。

### 2.2 主流程

```text
热点源产生 Signal
→ 提取主体、动作、对象、时间、地点和状态
→ 匹配 Candidate Cluster
→ 判断该来源的独立触发规则
→ 未命中：继续保留 Signal / Candidate Cluster
→ 命中：先匹配已有 Event
   ├─ 匹配成功：聚合到已有 Event
   └─ 匹配失败：创建新 Event
→ Event Card 增加来源与触发标签
```

三条热点源是“或”的关系，不要求共同命中。多个来源指向同一核心事件时只保留一个 Event。

## 3. X 热搜榜规则

### 3.1 采集

每 2 小时抓取以下五个地区榜单：

```text
Worldwide
美国
英国
日本
韩国
```

每个快照至少保存趋势词、地区、排名、快照时间、首次上榜时间和上一成功快照排名。采集失败不视为离榜，排名变化与最近一次成功快照比较。

### 3.2 七个直接调查大类

```text
AI
Technology
Politics & Elections
Geopolitics & Conflict
Macro & Financial Markets
Crypto & Web3
Prediction Markets
```

趋势词经语义识别命中任一大类，一上榜就立即调取相关信息，不附加排名、涨幅、持续时间或多地区门槛。同一趋势词可以拥有多个大类标签。

### 3.3 普通热搜

未命中七个大类的趋势词统一视为普通热搜。满足任一条件才启动调查：

```text
相邻两次成功快照排名上升至少 10 位
空降 Worldwide 或美国榜 Top 5
同一事件进入至少 2 个地区榜单
```

多地区上榜不要求趋势词文字相同；不同趋势词经最小语义调查后指向同一事件即可。

### 3.4 Event 形成

命中调查规则只表示必须理解发生了什么。系统调取相关内容后再创建或匹配 Event。一个趋势词可对应多个 Event，多个趋势词也可指向同一个 Event。无法解析出明确事件时保留未解析 Trend Signal。

### 3.5 标签

```text
X Trend
Top 5
Fast Rising
Persistent
Multi-region
Re-entry
```

排名、涨幅、持续时间和多地区表现是 Event 形成后的客观标签，不转化为高、中、低等级。

## 4. 关注圈层规则

### 4.1 采集与统计边界

- 5 个圈层共 59 个账号，每 2 小时增量抓取一次。
- 所有新帖子先保存为 Signal；账号所属圈层不限制帖子实际主题。
- 滚动窗口按帖子实际发布时间计算，不按抓取批次计算。
- 同一账号在同一窗口内多次讨论同一 Candidate Cluster，只贡献 1 个讨论账号。
- 多家媒体转述同一消息可以增加传播热度，但不增加事实独立性。

### 4.2 来源角色与权限

| 代码 | 来源角色 | 单点权限 |
|---|---|---|
| S1 | 第一方权威账号 | 发布自身权威范围内的重大事实时可直接创建或匹配 Event |
| S2 | 核心人物与决策者 | 明确宣布本人或所属机构的重大行动时可直接创建或匹配 Event |
| C | 专业媒体、快速雷达、数据、分析、预测和观点账号 | 先进入 Candidate Cluster，达到流量、圈内或跨圈规则后进入 Event |

S1/S2 权限只对帖子内容属于账号的 `authority_scope` 时生效。普通营销、日常运营、外部评论、转述、预测或闲聊进入 Candidate Cluster。

### 4.3 政治与选举圈：10 个

| 账号 | 主要角色 | 权限 | 权威范围 / 实现说明 |
|---|---|---|---|
| `@Reuters` | 专业新闻媒体 | C | 新闻报道 |
| `@AP` | 专业新闻媒体 | C | 新闻报道 |
| `@CNNPolitics` | 专业新闻媒体 | C | 政治新闻报道 |
| `@POLITICO` | 专业新闻媒体 | C | 政治新闻报道 |
| `@axios` | 专业新闻媒体 | C | 新闻报道 |
| `@thehill` | 专业新闻媒体 | C | 政治新闻报道 |
| `@nprpolitics` | 专业新闻媒体 | C | 政治新闻报道 |
| `@BBCWorld` | 专业新闻媒体 | C | 国际新闻报道 |
| `@DecisionDeskHQ` | 选举数据与快速雷达 | C | 选举数据、预测和结果判断不等于政府官方结果 |
| `@NateSilver538` | 分析、预测和观点 | C | 民调、预测、分析和观点 |

### 4.4 Crypto 与 Web3 圈：10 个

| 账号 | 主要角色 | 权限 | 权威范围 / 实现说明 |
|---|---|---|---|
| `@CoinDesk` | 专业新闻媒体 | C | Crypto 新闻报道 |
| `@Cointelegraph` | 专业新闻媒体 | C | Crypto 新闻报道 |
| `@cryptocom` | 第一方权威账号 | S1 | Crypto.com 自身产品、合作、监管、安全和经营变化 |
| `@WuBlockchain` | 快速聚合与市场雷达 | C | Crypto 快讯与市场信息 |
| `@tier10k` | 快速聚合与市场雷达 | C | 快讯和市场信息 |
| `@WatcherGuru` | 快速聚合与市场雷达 | C | 快讯和市场信息 |
| `@lookonchain` | 链上数据雷达 | C | 链上活动不自动等于现实事件 |
| `@BitcoinMagazine` | 专业新闻媒体 | C | Bitcoin 新闻与行业内容 |
| `@DecryptMedia` | 专业新闻媒体 | C | Crypto 新闻报道 |
| `@DefiLlama` | 数据与市场雷达 | C | DeFi 数据和市场变化 |

### 4.5 AI 与科技圈：19 个

| 账号 | 主要角色 | 权限 | 权威范围 / 实现说明 |
|---|---|---|---|
| `@OpenAI` | 第一方权威账号 | S1 | OpenAI 公司、模型和产品 |
| `@OpenAIDevs` | 第一方权威账号 | S1 | OpenAI API、开发者产品和 Codex 开发能力 |
| `@AnthropicAI` | 第一方权威账号 | S1 | Anthropic 公司、模型和产品 |
| `@claudeai` | 第一方权威账号 | S1 | Claude 产品 |
| `@GoogleDeepMind` | 第一方权威账号 | S1 | Google DeepMind 研究、模型和产品 |
| `@GoogleAI` | 第一方权威账号 | S1 | Google AI 研究和产品 |
| `@AIatMeta` | 第一方权威账号 | S1 | Meta AI、FAIR 和 Llama |
| `@spacexai` | 第一方权威账号 | S1 | xAI 公司、模型和产品 |
| `@deepseek_ai` | 第一方权威账号 | S1 | DeepSeek 公司、模型和产品 |
| `@Alibaba_Qwen` | 第一方权威账号 | S1 | Qwen 模型和产品 |
| `@cursor_ai` | 第一方权威账号 | S1 | Cursor 产品和服务 |
| `@nvidia` | 第一方权威账号 | S1 | NVIDIA 产品、芯片、合作和经营变化 |
| `@sama` | 核心人物与决策者 | S2 | 本人或 OpenAI 的明确重大行动 |
| `@thsottiaux` | 核心人物与决策者 | S2 | 本人负责范围内的 OpenAI 产品与 Codex 行动 |
| `@DarioAmodei` | 核心人物与决策者 | S2 | 本人或 Anthropic 的明确重大行动 |
| `@demishassabis` | 核心人物与决策者 | S2 | 本人或 Google DeepMind 的明确重大行动 |
| `@ylecun` | 分析、预测和观点 | C | AI 研究、分析和观点 |
| `@elonmusk` | 核心人物与决策者 | S2 | 本人或其所属公司的明确重大行动；普通评论不触发 S2 |
| `@TechCrunch` | 专业新闻媒体 | C | 科技新闻报道 |

### 4.6 宏观经济与金融圈：10 个

| 账号 | 主要角色 | 权限 | 权威范围 / 实现说明 |
|---|---|---|---|
| `@business` | 专业新闻媒体 | C | Bloomberg 新闻报道 |
| `@ReutersBiz` | 专业新闻媒体 | C | 商业与金融新闻报道 |
| `@CNBC` | 专业新闻媒体 | C | 财经新闻报道 |
| `@FinancialTimes` | 专业新闻媒体 | C | 财经新闻报道 |
| `@WSJ` | 专业新闻媒体 | C | 财经新闻报道 |
| `@TheEconomist` | 专业媒体与分析 | C | 新闻、分析和观点 |
| `@federalreserve` | 第一方权威机构 | S1 | 美联储政策、利率决定、会议和正式公告 |
| `@BLS_gov` | 第一方权威机构 | S1 | BLS 正式经济与就业数据 |
| `@KobeissiLetter` | 市场雷达与分析 | C | 市场快讯、数据解读和观点 |
| `@DeItaone` | 快速聚合与市场雷达 | C | 财经快讯和转述 |

### 4.7 预测市场圈：10 个

| 账号 | 主要角色 | 权限 | 权威范围 / 实现说明 |
|---|---|---|---|
| `@Polymarket` | 第一方权威账号 | S1 | Polymarket 产品、监管、合作、结算、安全和经营变化 |
| `@Kalshi` | 第一方权威账号 | S1 | Kalshi 产品、监管、合作、结算、安全和经营变化 |
| `@PolymarketIntel` | 社区新闻与快速雷达 | C | 新闻聚合；不是 Polymarket 公司第一方确认源 |
| `@OpinionLabsXYZ` | 第一方权威账号 | S1 | Opinion Labs 自身产品、合作和经营变化 |
| `@MyriadMarkets` | 第一方权威账号 | S1 | Myriad Markets 自身产品、合作和经营变化 |
| `@PredictIt` | 第一方权威账号 | S1 | PredictIt 自身产品、监管、结算和经营变化 |
| `@ZeitgeistPM` | 第一方权威账号 | S1 | Zeitgeist 自身产品、协议和经营变化 |
| `@PredictInsights` | 数据、分析和市场雷达 | C | 预测市场数据与分析 |
| `@ManifoldMarkets` | 第一方权威账号 | S1 | Manifold Markets 自身产品、规则和经营变化 |
| `@metaculus` | 第一方平台与预测数据 | S1 | Metaculus 自身产品、规则和经营变化；预测结果不是现实事实 |

预测市场平台新开某个外部事件市场，不等于外部事件已经发生。S1 只确认平台自身行动。

### 4.8 单点触发

满足任一条件即可由单条 Signal 创建或匹配 Event：

```text
S1 账号发布 authority_scope 内的重大事实
S2 账号明确宣布本人或所属机构的重大行动
Tmax ≥ 3，且该帖子进入账号近期相同帖龄表现前 5%
```

`Tmax` 是帖子在相同帖龄下的表现除以该账号近期帖子在相同帖龄下的正常表现。初始基线使用最近 30 条有效帖子的中位表现；优先使用浏览量，缺失时按转发与引用、回复、点赞的可用组合计算。

### 4.9 圈内共振

满足任一条件：

```text
B2h_circle ≥ 3
B24h_circle ≥ 6
B2h_circle ≥ 2 且 Tmax ≥ 2
```

- `B2h_circle`：滚动 2 小时内，同一圈层讨论同一 Candidate Cluster 的不同账号数。
- `B24h_circle`：滚动 24 小时内，同一圈层讨论同一 Candidate Cluster 的不同账号数。

### 4.10 跨圈扩散

满足任一条件：

```text
B4h_pool ≥ 3 且 C4h ≥ 2
B4h_pool ≥ 2 且 C4h ≥ 2 且 Tmax ≥ 2
B24h_pool ≥ 5 且 C24h ≥ 3
```

- `B4h_pool/B24h_pool`：滚动窗口内讨论同一 Candidate Cluster 的不同账号总数。
- `C4h/C24h`：这些账号覆盖的不同配置圈层数。

### 4.11 圈层标签

```text
Topic Circle
First-party
Executive Statement
Traffic Spike
In-circle
Cross-circle
Cross-circle Persistent
```

## 5. 未来事件规则

### 5.1 Action Score

| 维度 | 分值 |
|---|---:|
| 事件影响力 | 30 |
| 证据可靠度 | 20 |
| 热度动量 | 30 |
| 时间紧迫度 | 10 |
| 内容可执行性 | 10 |
| 合计 | 100 |

### 5.2 Event 门槛

```text
Action Score ≥ 80
→ 进入 Event 匹配
→ 已有同一 Event：聚合
→ 没有同一 Event：创建新 Event
```

低于 80 分继续保留在 Future Event 池中，持续更新证据、时间、热度和评分，不独立创建热点 Event。

80 分只控制 Future Event 能否独立进入 Event 层，不升级事实确认状态，也不自动生成、发布或撤回内容。

### 5.3 标签

```text
Future Event
Action Score 80+
Upcoming
Official Schedule
```

## 6. Event 聚合与关注权重

### 6.1 匹配维度

Event 匹配至少比较：

```text
主体
动作
对象
时间
地点
事件状态与事实含义
```

相同关键词、同一人物或同一长期主题不足以证明是同一个 Event。自动合并置信度由统一 Event 理解与合并规则维护，不在本文重复定义。

### 6.2 Event Card 标签

来源标签可以并存：

```text
X Trend
Topic Circle
Future Event
```

具体触发标签随来源追加。同一 Event 后续命中新来源时只更新标签、来源上下文和关注权重，不重复创建 Event。

### 6.3 权重边界

- 来源数量、跨区、圈内、跨圈、流量异常和 Future Event 分数可以增加内部关注权重。
- 关注权重用于 Event Card 排序、运营优先处理和持续跟踪。
- 关注权重不等于事实可信度；事实状态由 Evidence 与核验链路单独维护。
- 页面不展示由本规则计算的高、中、低热度等级。

## 7. 非目标与延后项

- 本文不定义每个趋势词抓取多少相关帖子或覆盖多长时间。
- 本文不定义 Event 理解、自动创建或自动合并的置信度门槛。
- 本文不定义内容生成、自动发布、活动执行或人工审核门禁。
- 本文不定义关注权重的数值公式；原型先展示来源和触发标签。

## 8. 开发验收

1. 五地区热搜和 59 个账号均按 2 小时频率增量采集，失败后从最近成功位置补齐。
2. 七个重点大类趋势词一上榜即进入调查；普通热搜只在三条规则任一命中时调查。
3. 59 个账号均具有唯一 `primary_role`、`single_trigger_policy` 和 `authority_scope` 配置。
4. S1/S2 只在帖子内容落入权威范围时单点触发；普通运营和外部评论进入 Candidate Cluster。
5. 单点、圈内、跨圈和 Future Event 80 分路径均可独立进入 Event 匹配。
6. 未达到门槛的 Signal 保留在 Candidate Cluster，窗口外内容不贡献当前热度。
7. 三类热点源命中同一事件时复用唯一 Event，并在 Event Card 上同时展示来源和触发标签。
8. 多来源与高热度不会自动提高事实确认等级，也不会自动发布内容。
