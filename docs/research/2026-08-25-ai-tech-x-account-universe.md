# AI 与科技 X 热点源账号池审计与扩展候选

日期：2026-08-25  
目标：为 PredX 建立一个能更快发现 AI/科技事件、同时保留第一方确认和产品早期线索的 X 账号池。本文仅做研究，不改动现有规格。

## 结论先行

现有 10 个账号适合作为“头部实验室公告 + 通用科技媒体”底座，但不够支撑实时热点发现：它缺少产品负责人、产品侦察/逆向发现、AI 专线记者、芯片与算力、快速聚合，以及中国/开源模型生态。

最值得立刻试跑的增量不是再加更多泛科技媒体，而是以下 14 个互补来源：

1. `@xai`、`@MistralAI`、`@deepseek_ai`、`@QwenLMChat`：补实验室和开源模型缺口；
2. `@sama`、`@demishassabis`、`@nickaturley`：补公司/产品负责人直接信号；
3. `@btibor91`、`@testingcatalog`：补 ChatGPT/Claude 等产品上线前后的代码、客户端和功能变化；
4. `@NVIDIA`、`@NVIDIAAI`：补芯片、算力和黄仁勋相关发布；
5. `@shiringhaffary`、`@kyliebytes`：补 AI 公司、人事、融资、政策等记者线索；
6. `@ArtificialAnlys`：补模型/API 性能、价格和可用性变化的数据证据。

建议不要把所有候选账号平权塞进一个固定“10 席位”圈。更合理的是分层：核心实时层 20–25 个账号，扩展观察层 20–30 个账号；用 2–4 周影子运行数据决定去留。

## 1. 现有账号池审计

规格当前配置：`@OpenAI`、`@AnthropicAI`、`@GoogleDeepMind`、`@AIatMeta`、`@huggingface`、`@AndrewYNg`、`@karpathy`、`@TechCrunch`、`@verge`、`@WIRED`。[现有规格](../../_bmad-output/specs/spec-topic-circle-radar/SPEC.md)

| 类型 | 现有覆盖 | 评价 |
|---|---|---|
| 头部实验室/产品官方 | OpenAI、Anthropic、Google DeepMind、Meta AI | 强，但漏 xAI、Microsoft AI、主要开源/中国模型实验室 |
| 高管/产品负责人 | 无（Andrew Ng、Karpathy 更接近专家/研究者） | 明显缺口；无法稳定捕获负责人先于机构号发布的产品语境 |
| 产品侦察/逆向发现 | 无 | 最大速度缺口之一 |
| 研究者/技术解释 | Andrew Ng、Karpathy | 有价值，但覆盖面窄、发帖并非持续事件流 |
| 开源/模型生态 | Hugging Face、Meta AI | 漏 Mistral、DeepSeek、Qwen、推理/部署生态 |
| 芯片/算力/云 | 无 | 漏 NVIDIA、AMD、云算力、数据中心与供应链事件 |
| 安全/评测/监管 | 无 | 漏模型事故、评测、政策变化；可先用少量高信号源补位 |
| AI 专线记者 | 无 | TechCrunch/The Verge/WIRED 是机构号，信息面广但不一定最早 |
| 快速聚合/数据雷达 | 无 | 无法利用跨公司扫描、模型价格/性能突变等快速信号 |

### 重叠问题

`@TechCrunch`、`@verge`、`@WIRED` 都是综合科技媒体，事件覆盖重叠较高，且机构号常晚于记者个人号。三者可以保留 1–2 个做主流扩散确认，把至少一个席位换成 AI 专线记者或产品侦察账号，增量价值更高。

`@OpenAI`、`@AnthropicAI`、`@GoogleDeepMind`、`@AIatMeta` 之间不是冗余：它们是不同主体的第一方发布，均有独立发现价值。

## 2. 覆盖分类与候选账号宇宙

符号：

- 速度：`S` 秒/分钟级、`M` 分钟/小时级、`L` 正式发布或深度解读；
- 原创：`高` 多为第一方或自身调查，`中` 原创与转述混合，`聚合` 主要扫描/提炼他人信号；
- 建议层：`核心` 建议进入高频监控，`观察` 先影子运行，`按需` 事件出现后查询。

### 2.1 官方实验室与产品

| 账号 | 角色 | 速度/原创 | 层级 | 增量价值与核验 |
|---|---|---|---|---|
| [@OpenAI](https://x.com/OpenAI) | OpenAI 官方 | S/高 | 核心 | 现有；发布模型、产品、API和公司公告。OpenAI 官网是其第一方事实源。[OpenAI](https://openai.com/) |
| [@OpenAIDevs](https://x.com/OpenAIDevs) | OpenAI 开发者官方 | S/高 | 核心 | API、模型和开发者产品发布，比公司总号更聚焦开发者热点；OpenAI 官方验证页列出该账号。[OpenAI Help](https://help.openai.com/en/articles/11725090-verifying-communications-from-openai) |
| [@ChatGPTapp](https://x.com/ChatGPTapp) | ChatGPT 产品官方 | S/高 | 核心 | 消费产品功能、上线和使用案例；OpenAI 官方验证页列出该账号。[OpenAI Help](https://help.openai.com/en/articles/11725090-verifying-communications-from-openai) |
| [@AnthropicAI](https://x.com/AnthropicAI) | Anthropic 官方 | S/高 | 核心 | 现有；Claude、Claude Code、安全和公司公告。[Anthropic News](https://www.anthropic.com/news) |
| [@GoogleDeepMind](https://x.com/GoogleDeepMind) | Google DeepMind 官方 | S/高 | 核心 | 现有；研究与模型，和消费产品发布仍有差异。 |
| [@GoogleAI](https://x.com/GoogleAI) | Google AI 产品/生态 | S/高 | 核心 | 补 Gemini、开发者和产品层，和 DeepMind 的研究层互补。 |
| [@AIatMeta](https://x.com/AIatMeta) | Meta AI 官方 | S/高 | 核心 | 现有；Llama 与 Meta AI。 |
| [@xai](https://x.com/xai) | xAI 官方 | S/高 | 核心 | 补 Grok、模型与基础设施；当前池完全缺失。 |
| [@MistralAI](https://x.com/MistralAI) | Mistral AI 官方 | S/高 | 核心 | 欧洲前沿实验室、开源/开放权重和产品发布。 |
| [@deepseek_ai](https://x.com/deepseek_ai) | DeepSeek 官方 | S/高 | 核心 | 中国前沿模型与开放权重；对全球模型竞争有明显增量。 |
| [@QwenLMChat](https://x.com/QwenLMChat) | Qwen 官方/团队账号 | S/高 | 核心 | 高频开放模型、Agent/多模态生态，弥补中国开源模型覆盖；正式入库前用用户信息接口再次固化账号 ID。 |
| [@MicrosoftAI](https://x.com/MicrosoftAI) | Microsoft AI 官方 | S/高 | 观察 | 补 Copilot 与自研 AI；与公司级 `@Microsoft`、OpenAI 信息有部分重叠。 |
| [@GeminiApp](https://x.com/GeminiApp) | Gemini 产品官方 | S/高 | 观察 | 消费产品功能和上线节奏，比 DeepMind 更贴近产品使用热点。 |

### 2.2 高管、产品负责人和关键建设者

| 账号 | 角色 | 速度/原创 | 层级 | 增量价值 |
|---|---|---|---|---|
| [@sama](https://x.com/sama) | OpenAI CEO Sam Altman | S/高 | 核心 | 经常补充机构公告没有的上线节奏、方向和公司语境；OpenAI 官方确认其 CEO 身份。[OpenAI leadership update](https://openai.com/index/leadership-updates-march-2025/) |
| [@nickaturley](https://x.com/nickaturley) | Nick Turley，ChatGPT 负责人 | S/高 | 核心 | 直接覆盖 ChatGPT 产品变化、功能采用和产品路线。OpenAI 官方称其为 VP & Head of ChatGPT。[OpenAI](https://openai.com/index/openai-acquires-software-applications-incorporated/) |
| [@thsottiaux](https://x.com/thsottiaux) | Thibault Sottiaux，OpenAI Codex/ChatGPT 产品建设者 | S/高 | 观察 | 经常直接发布或预告产品动态；这是另一个可能被简称为“Tibo”的人，不是 Tibor Blaho。OpenAI 系统卡贡献名单可核实其参与 OpenAI 产品。[OpenAI o1 system card](https://cdn.openai.com/pdf/o1-system-card.pdf) |
| [@demishassabis](https://x.com/demishassabis) | Google DeepMind CEO | S/高 | 核心 | 重大模型、研究和战略消息常有个人补充，和机构号互补。 |
| [@DarioAmodei](https://x.com/DarioAmodei) | Anthropic CEO | M/高 | 观察 | 公司战略、安全与政策主张；频率可能低于机构号。Anthropic 官方确认其 CEO/联合创始人身份。[Anthropic](https://www.anthropic.com/news/anthropic-infosys) |
| [@ylecun](https://x.com/ylecun) | Meta 首席 AI 科学家/研究领袖 | M/高 | 观察 | 研究方向与行业争论强，属于观点/研究信号，不等同 Meta 产品公告。 |
| [@satyanadella](https://x.com/satyanadella) | Microsoft CEO | M/高 | 观察 | 大型合作、基础设施和产品发布；泛公司内容较多。 |
| [@elonmusk](https://x.com/elonmusk) | xAI 创始人/关键发布者 | S/高 | 观察 | Grok/xAI 重大消息可能先发，但跨政治、SpaceX、X 等主题噪声极高，必须按帖分类。 |

**黄仁勋特别说明：**未找到 NVIDIA 官方社交目录列出的 Jensen Huang 个人 X 账号，不应监控同名仿冒号。用 `@NVIDIA`、`@NVIDIAAI` 和 NVIDIA 官方活动/新闻源承接黄仁勋演讲与发布。NVIDIA 官方列出的 X 账号包括 `@NVIDIA`、`@NVIDIAAI`、`@NVIDIAAIDev`。[NVIDIA 官方社交目录](https://www.nvidia.com/en-us/contact/social/)

### 2.3 产品侦察、逆向发现与发布前线索

| 账号 | 角色 | 速度/原创 | 层级 | 增量价值 |
|---|---|---|---|---|
| [@btibor91](https://x.com/btibor91) | Tibor Blaho，ChatGPT/Claude 产品侦察与逆向发现 | S/高 | 核心 | 若用户所说的“Tibo”是“提前发现 ChatGPT 隐藏功能的人”，高度可能是 **Tibor Blaho**。其本人 LinkedIn 明确链接 X handle `@btibor91`，并持续发布 ChatGPT 客户端代码、隐藏功能和模型线索。[本人 LinkedIn/X 链接](https://www.linkedin.com/posts/tiborblaho_tibor-blaho-btibor91-on-x-activity-7188063069288230912-ea96) |
| [@testingcatalog](https://x.com/testingcatalog) | AI 产品测试/客户端变化观察 | S/中高 | 核心 | 覆盖多个 AI 产品的灰度功能、界面和移动端变化，比官方发布更早，但需等待上线确认。 |

这类账号的独特价值是“提前量”，不是事实权威。输出状态应是 `产品线索/尚未正式发布`，官方发布后再升级为确认事件。

### 2.4 研究者与技术解释

| 账号 | 角色 | 速度/原创 | 层级 | 增量价值 |
|---|---|---|---|---|
| [@karpathy](https://x.com/karpathy) | 研究者/教育者/建设者 | M/高 | 核心 | 现有；能让新技术迅速形成开发者热点，但不承担全面新闻覆盖。 |
| [@AndrewYNg](https://x.com/AndrewYNg) | AI 教育与产业研究领袖 | L/高 | 观察 | 现有；解释和趋势价值高，突发发现速度一般。 |
| [@JeffDean](https://x.com/JeffDean) | Google 研究领袖 | M/高 | 观察 | 研究发布、人才和 Google 技术方向。 |
| [@fchollet](https://x.com/fchollet) | 研究者/ARC-AGI | M/高 | 观察 | 推理、评测和 AGI 争论，增量在基准与研究话题。 |
| [@DrJimFan](https://x.com/DrJimFan) | NVIDIA 研究者/技术解释者 | M/高 | 观察 | Agent、机器人、研究论文的快速技术解释；与 NVIDIA 官方公告不同。 |
| [@simonw](https://x.com/simonw) | 开发者/独立技术研究与验证 | S/高 | 核心 | 快速实测模型/API/工具，能将“发布”转成可验证的能力与限制。 |

### 2.5 开源模型与开发者生态

| 账号 | 角色 | 速度/原创 | 层级 | 增量价值 |
|---|---|---|---|---|
| [@huggingface](https://x.com/huggingface) | 模型/数据集/开源生态平台 | S/中高 | 核心 | 现有；覆盖面广，既有第一方产品也有生态聚合。 |
| [@ollama](https://x.com/ollama) | 本地模型运行工具官方 | S/高 | 观察 | 本地模型支持、新模型可用性和开发者采用信号。 |
| [@vllm_project](https://x.com/vllm_project) | 开源推理引擎官方 | S/高 | 观察 | 推理性能、模型支持和部署生态，属于基础设施早期信号。 |
| [@PyTorch](https://x.com/PyTorch) | AI 框架官方 | M/高 | 观察 | 框架重大版本与生态；日常突发率较低。 |

### 2.6 芯片、算力与云

| 账号 | 角色 | 速度/原创 | 层级 | 增量价值 |
|---|---|---|---|---|
| [@NVIDIA](https://x.com/NVIDIA) | NVIDIA 公司官方 | S/高 | 核心 | GPU、GTC、黄仁勋演讲、合作与公司级发布。NVIDIA 官方目录确认该 handle。[官方目录](https://www.nvidia.com/en-us/contact/social/) |
| [@NVIDIAAI](https://x.com/NVIDIAAI) | NVIDIA AI 官方 | S/高 | 核心 | 深度学习、AI 平台和模型/开发者生态；同一公司但与 `@NVIDIA` 内容侧重点不同。[官方目录](https://www.nvidia.com/en-us/contact/social/) |
| [@AMD](https://x.com/AMD) | AMD 官方 | S/高 | 观察 | AI 芯片竞争与新品；泛消费芯片内容会带来噪声。 |
| [@awscloud](https://x.com/awscloud) | AWS 官方 | M/高 | 观察 | 云模型、算力和重大合作；产品流量大，需按 AI 语境过滤。 |
| [@GoogleCloudTech](https://x.com/GoogleCloudTech) | Google Cloud 技术官方 | M/高 | 观察 | Vertex AI、TPU、云基础设施；与 Google AI/DeepMind 有互补。 |
| [@CoreWeave](https://x.com/CoreWeave) | AI 云/算力公司官方 | M/高 | 观察 | GPU 供给、数据中心、融资与大型算力合同。 |

### 2.7 安全、评测与监管

| 账号 | 角色 | 速度/原创 | 层级 | 增量价值 |
|---|---|---|---|---|
| [@METR_Evals](https://x.com/METR_Evals) | 前沿模型能力/风险评测机构 | M/高 | 观察 | 重大评测和风险研究；频率低但增量高。 |
| [@NIST](https://x.com/NIST) | 美国标准机构 | L/高 | 按需 | AI 标准与安全框架权威；更适合核验，不适合抢热点。 |
| [@EU_Commission](https://x.com/EU_Commission) | 欧盟委员会 | L/高 | 按需 | AI Act 与执法进展；泛政务噪声高，事件出现后查询更合适。 |
| [@HiddenLayerSec](https://x.com/HiddenLayerSec) | AI 安全公司/研究 | M/高 | 观察 | 模型与供应链漏洞、AI 安全事件；需与厂商公告/CVE核验。 |

### 2.8 AI 专线记者

记者个人账号的价值在于融资、人事、内部计划、监管谈判和产品时间线，常早于机构总号；但其爆料应保留“据报道”状态。

| 账号 | 已核实专线 | 速度/原创 | 层级 | 增量价值与来源 |
|---|---|---|---|---|
| [@shiringhaffary](https://x.com/shiringhaffary) | Bloomberg AI 记者 | S/高 | 核心 | 覆盖 OpenAI、Anthropic、融资、算力和政策。Bloomberg 作者页明确称其负责 AI。[Bloomberg](https://www.bloomberg.com/authors/AWgQvzatnYQ/shirin-ghaffary) |
| [@rachelmetz](https://x.com/rachelmetz) | Bloomberg AI 记者 | S/高 | 观察 | 模型公司、安全、法律和中国模型；Bloomberg 作者页标注 AI Reporter。[Bloomberg](https://bloomberg.com/authors/AWOWHOIGgDM/rachel-metz) |
| [@kyliebytes](https://x.com/kyliebytes) | AI/科技记者 | S/高 | 核心 | 前沿实验室、公司内部和产品动态；建议影子期核验相对现有机构号的领先时间。 |
| [@alexeheath](https://x.com/alexeheath) | 科技公司/AI 记者 | S/高 | 观察 | 高管、人事、平台战略和独家消息；部分覆盖泛科技。 |
| [@markgurman](https://x.com/markgurman) | Apple/消费科技记者 | S/高 | 观察 | Apple Intelligence、硬件和发布路线的高增量来源；仅在 Apple/消费 AI 是重点时纳入。 |

### 2.9 快速聚合与数据雷达

| 账号 | 角色 | 速度/原创 | 层级 | 增量价值 |
|---|---|---|---|---|
| [@ArtificialAnlys](https://x.com/ArtificialAnlys) | 模型/API 数据与基准 | S/高 | 核心 | 模型上线、价格、速度、上下文和基准的结构化变化；不是一般新闻聚合。 |
| [@TheRundownAI](https://x.com/TheRundownAI) | AI 新闻聚合 | S/聚合 | 观察 | 跨公司扫描快、标题可理解；与媒体/官方重叠高，事实需回溯。 |
| [@rowancheung](https://x.com/rowancheung) | AI 快讯/产品演示聚合 | S/聚合 | 观察 | 产品热点形成和大众传播信号强；原创证据能力较弱。 |

聚合账号应获得高“发现/传播”权重，但不能仅因多个聚合号复制同一消息而重复增加“事实确认”权重。

## 3. 推荐的核心实时层（第一轮 24 席）

建议先用以下结构替代“所有类型各塞一点、固定 10 个”的思路：

| 模块 | 建议账号 |
|---|---|
| 头部实验室/产品（10） | `@OpenAI`、`@AnthropicAI`、`@GoogleDeepMind`、`@GoogleAI`、`@AIatMeta`、`@xai`、`@MistralAI`、`@deepseek_ai`、`@QwenLMChat`、`@huggingface` |
| 负责人（3） | `@sama`、`@nickaturley`、`@demishassabis` |
| 产品侦察（2） | `@btibor91`、`@testingcatalog` |
| 技术验证/研究（2） | `@karpathy`、`@simonw` |
| 芯片算力（2） | `@NVIDIA`、`@NVIDIAAI` |
| 专线记者（2） | `@shiringhaffary`、`@kyliebytes` |
| 数据雷达（1） | `@ArtificialAnlys` |
| 主流科技媒体（2） | `@TechCrunch`、`@verge`（`@WIRED` 转观察层） |

这不是定稿名单，而是影子测试起点。若必须严格控制 20 个，可将 `@GoogleAI`、`@NVIDIAAI`、`@TechCrunch`、`@verge` 放入观察层；但不要删掉产品侦察和记者，它们正是现有池的主要速度增量。

## 4. 如何评价每个账号是否值得留下

影子运行 2–4 周后，对每个账号记录：

1. **有效事件贡献率**：其帖子最终形成明确事件的比例；
2. **首次发现贡献率**：它是否是池内第一个报告该事件的来源；
3. **平均领先时间**：相对机构官方号、主流媒体和最终确认的领先分钟数；
4. **原创/上游可追溯率**：是否给出公告、代码、文件、截图或第一方链接；
5. **热点命中率**：发现后是否有多个账号、互动或趋势信号跟进；
6. **重复度**：与其他账号报道同一批事件的比例；
7. **事件可理解性**：单帖能否识别主体、动作、对象和状态；
8. **误报/过度解释率**：尤其针对产品侦察、爆料和聚合账号；
9. **主题纯度**：AI/科技有效信号占其全部帖子的比例；
10. **运营转化率**：最终形成 PredX 可用内容机会的比例。

账号发帖只生成 Signal，不等于热点。进入热点候选仍需满足事件聚合、注意力异常或单帖相对爆发；第一方发布可直接提高事实确认状态，但不能自动证明公共热度。

## 5. 关键设计判断

- **发现和核验分开**：Tibor、TestingCatalog、记者和聚合号负责提前发现；官方账号、官网和文件负责确认。
- **热度和真实性分开**：多家媒体/聚合号转载应增加传播热度，但同一上游来源不能被算成多份独立证据。
- **产品侦察必须保留“未发布”状态**：代码或界面存在不代表功能必然上线。
- **同公司多账号只有在内容职责互补时保留**：如 `@NVIDIA`（公司/GTC）与 `@NVIDIAAI`（AI/开发者）可以并存；重复子号不应无限扩张。
- **黄仁勋用官方 NVIDIA 源监控**：不要为了“人物覆盖”误收仿冒个人账号。
- **记者不替代机构媒体**：记者提供提前量，机构号提供扩散确认；各保留少量即可。

## 6. 来源说明与限制

本文优先使用机构官网、本人职业资料、雇主作者页和机构官方社交目录核验角色；X handle 直接链接用于账号标识。平台账号、职位和活跃度会变化，正式写入配置前应通过现有用户信息接口再次检查账号 ID、简介、最近发帖和是否改名。

特别核验：

- Tibor Blaho 的本人 LinkedIn 帖子直接链接 `@btibor91`，并有持续 ChatGPT 产品侦察记录：[本人资料](https://www.linkedin.com/posts/tiborblaho_tibor-blaho-btibor91-on-x-activity-7188063069288230912-ea96)。
- Nick Turley 的 ChatGPT 负责人身份由 OpenAI 官方文章确认：[OpenAI](https://openai.com/index/openai-acquires-software-applications-incorporated/)。
- NVIDIA 官方社交目录确认 `@NVIDIA`、`@NVIDIAAI`、`@NVIDIAAIDev`，未列 Jensen Huang 个人 X 账号：[NVIDIA](https://www.nvidia.com/en-us/contact/social/)。
- Shirin Ghaffary 与 Rachel Metz 的 AI 专线身份由 Bloomberg 作者页确认：[Shirin](https://www.bloomberg.com/authors/AWgQvzatnYQ/shirin-ghaffary)、[Rachel](https://bloomberg.com/authors/AWOWHOIGgDM/rachel-metz)。
