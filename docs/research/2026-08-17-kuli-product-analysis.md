# Kuli 产品功能与逻辑研究

研究日期：2026-08-17  
研究范围：仅采用 Kuli 官网、Kuli 官方博客/Glossary 与 Kuli 官方 LinkedIn 等一手公开材料。官网中的效率、规模和效果数字属于厂商自述，未做客户侧或第三方验证。

## 一句话结论

Kuli 是面向品牌方与代理商 influencer/creator marketing 团队的 B2B AI agent：用户用自然语言提交 campaign brief，系统结合预先录入的品牌上下文，对大规模创作者视频、评论和受众信号做多模态分析，产出候选达人、品牌适配与风险判断、市场/竞品洞察、外联草稿，并持续监控上线内容。它卖的不是“更大的达人数据库”，而是把原本由人逐个看视频、查评论、做判断的内容理解和执行劳动自动化。[官网](https://kuli.one/) [官方产品逻辑说明](https://kuli.one/blog/ai-vs-traditional-influencer-marketing-platforms-2026/)

## 1. 产品定位与目标用户

### 官网明确的信息

- Kuli 自称营销团队的“AI co-worker”，目标是让团队在不增加 headcount 的前提下扩大 creator marketing 产出。[官网](https://kuli.one/)
- 核心对象是消费品牌的社媒、达人营销团队，以及同时服务多个品牌/项目的代理商。官网把 Kuli 与 agencies、传统 influencer platforms 对比；官方 LinkedIn 则直接称其服务 enterprise consumer social media and influencer marketing teams。[官网](https://kuli.one/) [官方 LinkedIn](https://www.linkedin.com/company/kuliai)
- 页面展示的信任品牌/机构包括 Armani Beauty、Havas Play、Supercell、Disney、Microsoft、Monks、Roland Garros、PostHog、Upway；这只能证明官网展示了这些 logo，不能单独证明每家当前的合同范围或使用深度。[官网](https://kuli.one/)

### 推断出的最适合场景

- 已有一定 creator 投放规模、但团队审核与洞察产能不足的中大型品牌。
- 需要频繁为不同客户做发现、筛选、风险审核和竞品研究的 agency。
- 尤其适合视频优先、趋势变化快、品牌安全敏感的消费行业，例如美妆、护肤、游戏、娱乐。
- 不明显适合只偶尔做少量达人合作、主要痛点在合同/付款/CRM 的小团队，因为 Kuli 官方也承认传统平台在关系管理、合同付款和长期历史分析上仍有优势。[官方产品逻辑说明](https://kuli.one/blog/ai-vs-traditional-influencer-marketing-platforms-2026/)

## 2. 主要功能

### 2.1 品牌上下文层

首次装载品牌支柱、禁区、历史 campaign、语气、受众及过往经验；之后搜索、分析和文案草拟都经过这套上下文，避免每次任务从零提示。[官网](https://kuli.one/)

这层是整套系统的“长期记忆/策略约束”：同一个创作者或视频，对不同品牌可能得到不同的适配与风险结论。

### 2.2 自然语言找达人与内容优先的筛选

- 用户可以输入 URL、creator 或 campaign brief；Kuli 分析视频的 hook、音频、节奏、caption、品牌适配和受众响应。[官网](https://kuli.one/)
- 用户可以直接描述内容特征和目标，而不是只用粉丝量、互动率、地域等结构化过滤器；官方示例是寻找符合特定审美、话题表达方式、受众与粉丝规模的 micro-influencers。[官网](https://kuli.one/) [官方产品逻辑说明](https://kuli.one/blog/ai-vs-traditional-influencer-marketing-platforms-2026/)
- 系统按实际内容信号匹配和排序，官方称会看内容质量、受众真实性、主题深度、制作轨迹与成长潜力，并试图比传统数据库更早发现 emerging creators。[官方 Discovery Intelligence 定义](https://kuli.one/glossary/discovery-intelligence/)

### 2.3 视频与内容表现拆解

Kuli 不只返回达人名单，还解释某条内容为什么表现好：逐段/逐帧提取 hook、镜头与剪辑节奏、音频趋势、caption、内容调性、产品植入方式，以及评论中的受众意图。[官网](https://kuli.one/)

这意味着结果形态更像“带理由和证据的 analyst brief”，而非只有一组指标的 profile 卡片。

### 2.4 Look-alike creators

用户标记一个有效创作者后，系统可按审美、受众重叠和内容发布节奏寻找相似创作者，而非只按 follower count 或泛化标签找相似对象。[官网](https://kuli.one/)

### 2.5 趋势、竞品与行业情报

- 持续跟踪指定竞品或行业品牌近期发布、付费合作和内容表现，并在 dashboard 做横向对比。[官网](https://kuli.one/)
- 流式观察大量新帖，识别跨 feed 的内容格式、增长速度、评论里的购买/询问意图等信号，并形成 trend radar。[官网](https://kuli.one/)
- 官方活动复盘称，用户可以用简单 prompt 找品牌适配达人、发现 viral trends、追踪竞品活动和分析 performance signals。[官方活动复盘](https://kuli.one/blog/kuli-at-paris-creator-week/)

### 2.6 Brand safety、合规审核与持续监控

- 对每个视频逐帧分析，并结合品牌自定义规则检查竞品露出、争议符号/场景、品牌价值观、音频/歌词、背景对话、屏幕文字、caption、视觉上下文、广告披露/行业规则、情绪与语调。[Brand Safety 产品页](https://kuli.one/brand-safety/)
- 输出可执行报告：时间戳、画面证据、风险分类和批准建议；人只需要复核被标记的部分。[Brand Safety 产品页](https://kuli.one/brand-safety/)
- 内容发布后仍继续监控，越界时实时提醒；它将品牌安全从一次性 pre-vetting 延伸到上线后的持续检查。[Brand Safety 产品页](https://kuli.one/brand-safety/) [官方产品逻辑说明](https://kuli.one/blog/ai-vs-traditional-influencer-marketing-platforms-2026/)
- 官网宣称完整分析约 2–3 分钟、可处理 unlimited content、无需信用卡试用、2 分钟设置、enterprise-grade security 且 SOC 2 compliant；这些均为厂商页面陈述，公开材料未提供审计报告或服务条款细节供本次核验。[Brand Safety 产品页](https://kuli.one/brand-safety/)

### 2.7 外联与报告

官网明确写到 discovery、vetting、outreach、reporting/ROI 会由 Kuli 处理，并会按品牌语气起草个性化 outreach；首页还支持 same-day asks、scheduled routines 和 hourly refreshes 并行运行。[官网](https://kuli.one/)

但公开页面没有展示完整的邮件发送、审批、回复管理、合同、付款和 CRM 工作流，因此“处理 outreach”目前应谨慎理解为至少能生成草稿，是否可直接发送和持续管理关系需 demo 验证。

### 2.8 免费工具与获客入口

官网提供 TikTok/Instagram engagement rate、influencer pricing、EMV 等免费计算器，并宣称可免费分析 creator content。[免费工具页](https://kuli.one/tools/) [TikTok Engagement Calculator](https://kuli.one/tools/tiktok-engagement-calculator/) [Influencer Pricing Calculator](https://kuli.one/tools/influencer-pricing-calculator/) [EMV Calculator](https://kuli.one/tools/emv-calculator/)

从产品经营逻辑看，这些工具同时承担 SEO、教育用户和低门槛获客作用：先承接用户搜索互动率、报价、EMV 等传统指标，再引导用户接受 Kuli 的主张——单一指标不够，需要实际内容理解。

### 2.9 Shopify 效果归因闭环

Kuli 的 Privacy Policy 明确列出 Shopify 的 `read_orders`、`read_products`、`read_discounts`、`write_discounts` 权限：用于通过 discount code / affiliate link 归因销售，计算 revenue、conversion、AOV 与 product performance，管理折扣码生命周期，并在 campaign dashboard 展示指标。[Privacy Policy](https://kuli.one/privacy-policy/)

这是理解产品边界的重要证据：官网首页所说的 reporting/ROI 不只是内容层的 EMV 或互动统计，至少对 Shopify 商家可以连到实际订单与营收。政策同时称 Shopify 数据存储在欧盟爱尔兰，主要托管基础设施是 Microsoft Azure。[Privacy Policy](https://kuli.one/privacy-policy/)

## 3. 核心工作流

可将公开材料还原为以下闭环：

1. **品牌初始化**：录入品牌支柱、目标受众、历史 campaign、语气、禁区、竞品与合规规则。
2. **任务发起**：在聊天界面输入 campaign brief、目标 creator 描述、一个 URL/creator，或提出竞品/趋势研究问题。
3. **并行内容分析**：多个 AI agent 分别分析内容表达与定位、受众互动、品牌安全、真实性和表现潜力；核心输入不只含 profile metadata，而含视频画面、音频、字幕、caption 与评论。[官方产品逻辑说明](https://kuli.one/blog/ai-vs-traditional-influencer-marketing-platforms-2026/)
4. **排序与解释**：给出 shortlist、fit/risk 判断及证据，解释为什么符合品牌和为什么内容有效。
5. **人工决策**：营销人员负责选择、创意判断与异常复核；产品定位不是完全取消 human-in-the-loop，而是把人从大规模重复观看中释放出来。[官网](https://kuli.one/)
6. **执行协助**：生成品牌语气的个性化外联草稿，支持定时任务和周期刷新。
7. **上线后闭环**：持续监控发布内容、竞品与趋势，触发告警并沉淀 campaign 数据，供下一轮品牌上下文和判断使用。
8. **交易归因（Shopify 商家）**：用折扣码或 affiliate link 将订单归因到 creator/campaign，回传营收、转化率、AOV 与商品表现。[Privacy Policy](https://kuli.one/privacy-policy/)

## 4. 底层产品逻辑

### 4.1 从“profile database”转向“content intelligence”

传统平台先聚合达人资料，再用地区、粉丝量、互动率、历史合作等字段过滤；Kuli 的差异化主张是先理解创作者实际发布的视频，再按任务目标匹配。它认为两个 profile 指标近似的达人，可能有完全不同的讲述方式、产品植入能力和品牌价值。[官方产品逻辑说明](https://kuli.one/blog/ai-vs-traditional-influencer-marketing-platforms-2026/)

### 4.2 多模态分析是核心技术资产

系统把视觉、音频、文本、评论和时间序列内容整合为 creator content profile，再把这一层用于发现、适配、品牌安全、趋势和表现解释。官方称其使用 large language vision models 并对数百万 creator videos 做分析。[官方 Brand Safety 深入说明](https://kuli.one/blog/influencer-brand-safety-ai-video-analysis/) [官方 Discovery Intelligence 定义](https://kuli.one/glossary/discovery-intelligence/)

### 4.3 Agent orchestration 是交互与运营层

产品不是要求用户手动操作大量筛选器，而是通过聊天式 brief 触发多个并行子任务；用户主要负责设定意图、复核 shortlist 与做最终判断。定时例行任务、小时级刷新和持续监控则让它从一次性分析工具变成运营系统。[官网](https://kuli.one/)

### 4.4 学习飞轮（推断）

官网称系统基于品牌、受众和历史 campaign 进行个性化，并“learning from each campaign”。合理推断其飞轮是：更多视频与评论分析 → 更丰富的内容模式；更多品牌规则与人类 shortlist/approval 反馈 → 更好的品牌适配；更多 campaign 结果 → 更好的排序与表现预测。[官网](https://kuli.one/) [官方产品逻辑说明](https://kuli.one/blog/ai-vs-traditional-influencer-marketing-platforms-2026/)

这仍是产品机制推断；公开资料没有说明模型是否真正在线训练、反馈如何进入模型、客户数据是否隔离。

## 5. 商业模式与增长逻辑

- **企业级 SaaS / sales-led**：首页价格写为 **from US$2,000/month，unlimited volume**，主要 CTA 为 Book a Demo/Talk to sales，而非透明的自助订阅阶梯。[官网](https://kuli.one/)
- **价值定价锚点**：不是按达人数量卖数据库访问权，而是用“无需增加 headcount、并行无限处理、分钟级结果”对比代理商月费 US$15k–50k 和传统平台 US$5k–15k 的官网估算。[官网](https://kuli.one/)
- **单位经济主张**：固定起步订阅 + unlimited volume 会鼓励高频、广覆盖使用；客户处理规模越大，替代的人工审查和研究时数越多，ROI 越容易成立。但官网没有披露 fair-use、算力上限或附加席位/服务费。
- **产品主线 + 独立 wedge**：完整 AI agent 覆盖 discovery 到 outreach/reporting；Brand Safety 页面又以明确痛点、免费试用和 SOC 2 声明作为单独切入口，可能更易通过风控/合规预算进入大客户。
- **内容与工具获客**：双语官网、Glossary、长篇教育内容和免费计算器形成 SEO funnel；工具承接传统指标需求，文章再教育用户转向内容智能与 demo。
- **公司主体**：Privacy Policy 所列控制方为法国 Kuli SAS（Nanterre 注册号 930 631 080，地址在 Levallois-Perret）。[Privacy Policy](https://kuli.one/privacy-policy/)

## 6. 官网主张的数据，应如何解读

- 官网自述：Kuli 可让 creator marketing “10× faster”、从一次 brief 在分钟内出结果、并行 unlimited volume。[官网](https://kuli.one/)
- 官方博客自述：使用 Kuli 的团队在同等团队规模下能产出 3 倍 collaborations。[官方产品逻辑说明](https://kuli.one/blog/ai-vs-traditional-influencer-marketing-platforms-2026/)
- 官方 LinkedIn 自述：客户把 sourcing 从 days 降到 minutes，并在相同预算下做到 2× creator collaborations；另有项目称 influencer vetting 时间下降超过 90%。[官方 LinkedIn 公司页](https://www.linkedin.com/company/kuliai)

这些数据口径不一致，且缺少样本、基线、时间范围和独立客户 case study，因此可当价值假设，不宜直接当已验证 benchmark。

## 7. 尚未被公开资料讲清楚的问题

建议 demo 时重点追问：

1. **平台覆盖**：公开材料明确点名 TikTok 和 Instagram，但“across platforms/every feed”没有完整平台、国家和语言清单。[Creator Content Profile](https://kuli.one/blog/creator-content-profile/) [Privacy Policy](https://kuli.one/privacy-policy/)
2. **数据获取合法性与稳定性**：视频、评论、受众人口统计、赞助关系和竞品付费信息来自官方 API、授权数据商还是公开抓取？刷新频率和历史深度是多少？
3. **规模定义**：所谓 millions of videos、499 posts/min、unlimited volume 是全局索引规模、实时吞吐还是界面演示数字？单客户是否有额度/FUP？
4. **结果可信度**：fit score、performance delta、audience overlap、bot/real fan 比例和趋势提前量如何计算？有无 precision/recall、置信度、可追溯原始证据和人工 override？
5. **Brand Safety 误报/漏报**：规则如何配置？敏感文化语境如何处理？“regulatory compliance”和“music rights verification”覆盖哪些司法辖区与版权库？
6. **Human-in-the-loop**：外联是否仅起草，还是可直接发送？批准链、权限、审计日志和误发保护如何做？
7. **Campaign ops 边界**：是否包含 CRM、contracting、content approval、payment、affiliate tracking、sales attribution？官方比较文章暗示这些仍是传统平台强项。
8. **数据安全**：SOC 2 的具体类型、审计范围、数据驻留、保留与删除策略、客户数据是否用于模型训练、第三方模型供应商是谁？
9. **集成**：已确认 Shopify；是否还有公开 API，以及能否连接邮箱、Slack/Teams、CRM、BI、creator management 与 paid media 系统仍不清楚。
10. **定价细则**：US$2,000/月包含多少品牌、席位、地区、历史数据与 onboarding？Brand Safety 是否单独收费？是否有年度承诺与服务费？

## 8. 最终判断

Kuli 的真正产品创新点不是“用 AI 帮你搜达人”，而是把视频内容本身做成可查询、可比较、可持续监控的数据层，然后在上面运行品牌定制的 agent。其潜在护城河来自跨模态 creator content graph、品牌上下文积累、任务反馈和持续扫描能力；其最大风险则是底层社交数据访问、分析结果可验证性、合规结论责任边界，以及“unlimited”在高算力视频分析下的可持续单位经济。

从公开材料看，它更像传统 influencer suite 之前/之上的“内容智能与执行层”，而不是已经完整替代关系管理、合同、付款、归因等 campaign operating system 的全栈平台。
