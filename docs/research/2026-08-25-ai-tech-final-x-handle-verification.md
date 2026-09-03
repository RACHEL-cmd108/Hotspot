# AI / 科技第一批 X 账号最终核验

核验日期：2026-08-25  
对象：此前拟定的 21 个 X handle  
方法：优先用公司官网、官方帮助中心、官方产品页及官方账号之间的交叉引用确认身份；再用当前 X 公开资料和 GrowthOps 只读账号卡确认账号可解析、活跃状态与创建时间。蓝标只作辅助信号，不单独视为官方身份凭证。

## 结论

原名单并非全部正确：**2 个 handle 必须替换，2 个身份说明需要调整**。

1. `@xai` → **`@spacexai`**。xAI 官网当前在 Social 一栏明确链接 `@spacexai` 和 `@grok`；旧 `@xai` 不应继续作为公司主账号监控。[xAI 官网](https://x.ai/)
2. `@QwenLMChat` → **`@Alibaba_Qwen`**。`@QwenLMChat` 当前无法由 X 数据接口解析；Qwen 当前官方发布账号为 `@Alibaba_Qwen`。[Qwen 官方 Hugging Face 组织页](https://huggingface.co/Qwen)、[当前 Qwen X 账号](https://x.com/Alibaba_Qwen)
3. `@ylecun` 的 handle 正确，但“Meta 首席 AI 科学家”已经过期。当前应标注为 **AMI Labs 联合创始人、执行主席 / 高声量 AI 科学家**。[Yann LeCun 本人主页](https://yann.lecun.com/)、[AMI Labs 官网](https://amilabs.xyz/)
4. `@thsottiaux` 的 handle 正确，但建议描述为 **OpenAI 产品负责人，重点覆盖 Codex**。第一方资料能确认他领导 Codex，不宜未经证据扩大为负责 OpenAI 全部 ChatGPT、Codex 和 API 产品。[OpenAI Forum](https://forum.openai.com/public/events/codex-is-for-everyone-why-codex-matters-beyond-code-fa40puy7wi?autoRsvp=true)

修订后仍是 21 个账号。

## 逐项核验

| 原 handle | 结论 | 当前身份 / 用途 | 一手或直接证据 | 风险提示 |
|---|---|---|---|---|
| `@OpenAI` | 保留，确认官方 | OpenAI 公司主账号 | OpenAI 官方通信核验页明确列出该账号。[OpenAI Help](https://help.openai.com/en/articles/11725090-verifying-communications-from-openai) | 无明显风险 |
| `@ChatGPTapp` | 保留，确认官方 | ChatGPT 产品账号 | OpenAI 官方通信核验页明确列出。[OpenAI Help](https://help.openai.com/en/articles/11725090-verifying-communications-from-openai) | 本次第三方 user lookup 返回 `user not found`，但 OpenAI 2026 年更新的官方清单仍明确承认；应按官方清单保留，同时在接入时用 X user ID 再核一次 |
| `@OpenAIDevs` | 保留，确认官方 | OpenAI 开发者 / API 更新 | OpenAI 官方通信核验页及 API 帮助页均明确列出。[OpenAI Help](https://help.openai.com/en/articles/11725090-verifying-communications-from-openai)、[API Help](https://help.openai.com/en/articles/4936851-how-do-i-start-exploring-the-openai-api) | 无明显风险 |
| `@AnthropicAI` | 保留，确认官方 | Anthropic 公司主账号 | 账号简介链接 `anthropic.com` 并指向产品号 `@claudeai`。[X](https://x.com/AnthropicAI/with_replies) | 注意仿冒号 `@Anthropic_ai` 等 |
| `@claudeai` | 保留，确认官方 | Claude 产品账号 | 简介明确“built by @AnthropicAI”，并链接 `claude.ai`；与公司号互引。[X](https://x.com/claudeai/with_replies) | 2025 年新建，但已形成明确官方交叉引用 |
| `@GoogleDeepMind` | 保留，确认官方 | Google DeepMind 公司、研究与模型发布 | 当前账号持续发布 DeepMind 一手研究与产品信息。[X](https://x.com/GoogleDeepMind) | GrowthOps 当前未显示蓝标；不影响官网身份和长期账号历史 |
| `@GoogleAI` | 保留，确认官方 | Google AI 广义研究和产品动态 | 当前 Google AI 官方账号持续发布 Google AI 研究内容。[X](https://x.com/GoogleAI) | 它不是 Gemini 单一产品号；分类时不要把所有帖子都标成 Gemini 更新 |
| `@AIatMeta` | 保留，确认官方 | Meta AI / FAIR | Meta 的旧账号 `@metaai` 简介明确写明已迁移并要求关注 `@AIatMeta`。[旧账号迁移说明](https://x.com/metaai/with_replies)、[当前账号](https://x.com/AIatMeta) | 无明显风险 |
| `@xai` | **替换** | 旧 handle，不再是当前公司主账号 | xAI 官网当前 Social 链接为 `@spacexai`。[xAI 官网](https://x.ai/) | 当前数据接口解析到的 `@xai` 仅 0 粉丝且账号年龄很短，极可能是释放后重新注册的 handle；不可继续监控 |
| `@deepseek_ai` | 保留，确认官方 | DeepSeek 唯一官方 X 账号 | DeepSeek 官方 Google Play 应用详情明确列出 Twitter `@deepseek_ai`。[Google Play](https://play.google.com/store/apps/details?id=com.deepseek.chat) | DeepSeek 曾专门警告大量仿冒账号；必须保存 user ID |
| `@QwenLMChat` | **替换** | 旧 handle / 当前不可解析 | 当前官方账号为 `@Alibaba_Qwen`。[Qwen 官方组织](https://huggingface.co/Qwen)、[X](https://x.com/Alibaba_Qwen) | 账号发生过更名；规则和数据库都应改用新 handle 并保存 user ID |
| `@cursor_ai` | 保留，确认官方 | Cursor 产品账号 | Cursor 官网 Connect 区直接链接其 X 账号。[Cursor 官网](https://cursor.com/)、[X](https://x.com/cursor_ai) | 无明显风险 |
| `@nvidia` | 保留，确认官方 | NVIDIA 公司主账号 | 账号简介明确为 NVIDIA official handle，并链接 NVIDIA 官网及全部社媒入口。[X](https://x.com/nvidia/with_replies) | 无明显风险；可作为黄仁勋个人号的稳定备份来源 |
| `@sama` | 保留，确认本人 | Sam Altman，OpenAI CEO | 长期本人账号，与 OpenAI 官方账号及公告体系持续互引。[X](https://x.com/sama) | 高声量且包含个人观点，帖子类型需区分“公司公告”与“个人判断” |
| `@thsottiaux` | 保留，确认本人 | Thibault “Tibo” Sottiaux，OpenAI 产品负责人，重点 Codex | OpenAI Forum 明确确认其为 OpenAI 成员并领导 Codex。[OpenAI Forum](https://forum.openai.com/public/events/codex-is-for-everyone-why-codex-matters-beyond-code-fa40puy7wi?autoRsvp=true)、[X](https://x.com/thsottiaux) | 身份描述不要扩写成“负责 OpenAI 所有核心产品” |
| `@DarioAmodei` | 保留，确认本人 | Dario Amodei，Anthropic 联合创始人兼 CEO | Anthropic 官方活动页确认其身份；账号长期发布本人文章并与 Anthropic 账号互引。[Anthropic](https://www.anthropic.com/events/builder-summit-bengaluru)、[X](https://x.com/DarioAmodei) | 发帖量低于公司账号，但仍有第一方价值 |
| `@demishassabis` | 保留，确认本人 | Demis Hassabis，Google DeepMind 联合创始人兼 CEO | X 简介明确关联 `@GoogleDeepMind`，并与公司账号长期互引。[X](https://x.com/demishassabis/with_replies)、[Google DeepMind](https://deepmind.google/about/) | 无明显风险 |
| `@ylecun` | 保留，身份说明更新 | Yann LeCun，AMI Labs 联合创始人、执行主席；高声量 AI 科学家 | 本人主页当前列为 AMI Labs Executive Chairman，AMI 官网列为创始团队成员。[本人主页](https://yann.lecun.com/)、[AMI Labs](https://amilabs.xyz/) | **不能再写 Meta 首席 AI 科学家**；其发言多为观点与研究判断，不等于公司公告 |
| `@elonmusk` | 保留，确认本人 | Elon Musk；xAI / SpaceX / Tesla 等重大科技与舆论信号 | 长期本人账号，并与其公司官方账号持续互引。[X](https://x.com/elonmusk) | 信息跨度极广，必须按实体和事件分类，不能把全部发帖自动归入 AI 热点 |
| `@JensenHuang` | 保留，但加强身份锁定 | Jensen Huang，NVIDIA 创始人兼 CEO；2026 年 6 月新开的个人号 | 当前账号简介链接 NVIDIA 官方人物页，身份、发言内容及 NVIDIA 官方账号交叉互动一致。[X](https://x.com/JensenHuang/with_replies)、[NVIDIA 官方人物页](https://nvidianews.nvidia.com/bios/jensen-huang) | 第一方交叉证据足以纳入监控，但它是新号，历史远短于其他人物号；入库时必须固定 X user ID，并保留 `@nvidia` 作为稳定验证源 |
| `@TechCrunch` | 保留，确认官方 | TechCrunch 科技媒体账号 | 账号链接 TechCrunch 官方站并长期发布该站内容。[X](https://x.com/TechCrunch/with_replies)、[官网](https://techcrunch.com/) | 媒体发现源，不是事件真实性的最终确认源 |

## 修订后的 21 个账号

```text
@OpenAI
@ChatGPTapp
@OpenAIDevs
@AnthropicAI
@claudeai
@GoogleDeepMind
@GoogleAI
@AIatMeta
@spacexai
@deepseek_ai
@Alibaba_Qwen
@cursor_ai
@nvidia
@sama
@thsottiaux
@DarioAmodei
@demishassabis
@ylecun
@elonmusk
@JensenHuang
@TechCrunch
```

## 入库建议

- 不要只保存 handle；同时保存 X `user_id`、显示名、官网域名和最近核验时间。handle 会更名或被释放。
- 账号权威性分为：公司官网直接列出、官方账号互引、本人账号与公司账号交叉确认、仅有蓝标。蓝标不能单独证明身份。
- `@ChatGPTapp` 在当前第三方查询中有解析异常，接入前单独做一次 user ID lookup；在 OpenAI 官方清单未移除它之前，不应仅因第三方报错而删除。
- `@JensenHuang` 是新号，建议以 `@nvidia` 的引用/转发和固定 user ID 共同验证，避免未来 handle 被冒用。
