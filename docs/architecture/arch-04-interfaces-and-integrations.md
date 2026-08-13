# 04 接口与集成

## 内部命令与事件

| 生产者 | 事件 | 消费者 | 语义 |
| --- | --- | --- | --- |
| Discovery | `candidate_event.qualified.v1` | Event Intelligence | 合格信号进入事件聚合。 |
| Event Intelligence | `event.response_rule_matched.v1` | Content Response | 创建或维持一个合规 ART。 |
| Content Response | `publication.recorded.v1` | Outcome & Learning | URL/失败原因被人工回填。 |
| Event Intelligence | `event_card.materially_changed.v1` | M3、M4 | 冻结待执行下游并复核。 |
| Configuration | `config_version.published.v1` | M1、M3、M4 | 仅影响后续新工作；历史引用不改写。 |

## 外部端口

| 端口 | 当前用途 | 不变量 |
| --- | --- | --- |
| Google Identity | Workspace 登录与受信任身份 | 验证 issuer、audience、签名、过期时间和允许域；不保存本地密码。 |
| X Read API | 五地区趋势、地区前三来源、后续效果读取 | 限流、凭据轮换、来源原链接和采集错误可见；当前不使用 X 写入 API 发帖。 |
| AI Generation | 账号专属候选与活动方案草稿 | 仅传公开资料、确认事实、来源链接和已发布配置；输出进入预检与人工操作。 |

所有外部调用由 Worker 执行，并记录请求相关性、尝试次数、错误分类和幂等键。超时/未知结果不得把外部状态当作成功；当前人工 X 发布无系统写入副作用，未来启用写入端口须先落实 AD-13 的消歧规则。
