# 04 接口与集成

## 内部命令与事件

| 生产者 | 事件 | 消费者 | 语义 |
| --- | --- | --- | --- |
| Discovery | `candidate_event.qualified.v1` | Event Intelligence | 合格信号进入事件聚合。 |
| Event Intelligence | `event.response_rule_matched.v1` | Content Response | 创建或维持一个合规 ART。 |
| Content Response | `content_generation.requested.v1` | Content Response Worker | 带 ART、Generation Run、Event Card 与配置快照的生成请求。 |
| Content Response | `content_generation.discarded_stale.v1` | 审计/运维 | 迟到结果被拒收，不改变可选候选。 |
| Content Response | `publication.recorded.v1` | Outcome & Learning | URL/失败原因被人工回填。 |
| Event Intelligence | `event_card.materially_changed.v1` | M3、M4 | 冻结待执行下游并复核。 |
| Event Intelligence | `event_resolution.auto_merged.v1` | M3、M4 | 携带置信度、依据、前后版本和受影响对象分类；仅 `review_required` 候选冻结。 |
| Configuration | `config_version.published.v1` | M1、M3、M4 | 仅影响后续新工作；历史引用不改写。 |

## 外部端口

| 端口 | 当前用途 | 不变量 |
| --- | --- | --- |
| Google Identity | Workspace 登录与受信任身份 | 验证 OIDC issuer、audience、签名、过期/签发时间、nonce 和允许域；以 `sub` 为内部用户稳定键，邮箱只作可变展示/域策略字段。 |
| X Trends | `GET /2/trends/by/woeid/{id}` 取得五个配置 WOEID 的趋势快照 | 固定 WOEID 清单、`max_trends=30`、采集时间、返回原始趋势名/计数和错误；趋势地区只表示该趋势出现地。 |
| X Post Search | `GET /2/tweets/search/recent` 为每个合格趋势检索最近 7 天帖子 | 查询由规范化趋势名生成，记录完整 query、时间窗口、排序策略、返回的前三条和实际数量；不把搜索结果或趋势地区推定为发帖者地理位置。 |
| X Metrics | Post lookup 请求 `public_metrics`；自有账号有授权时可补充非公开指标 | 指标快照保存数据源、授权类型、采样时间和窗口；缺失/权限不足为数据状态，不填零。 |
| AI Generation | 账号专属候选与活动方案草稿 | 输入仅含公开资料、确认事实、来源链接和已发布配置；输出必须带 `schema_version`、run ID、候选文本、引用来源 ID、限制/风险标记和模型元数据；输出进入预检与人工操作。 |

所有外部调用由 Worker 执行，并记录请求相关性、尝试次数、错误分类和幂等键。X Trends 和 Search 是两个独立调用，Search 失败不得伪装为“没有来源”。超时/未知结果不得把外部状态当作成功；当前人工 X 发布无系统写入副作用，未来启用写入端口须先落实 AD-13 的消歧规则。
