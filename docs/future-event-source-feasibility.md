# 未来事件源接入可行性

未来事件中心以小而可靠的事件池起步。每个来源注册为独立 Connector 或 Rule Set，并统一产出 Event、Evidence Record、Confirmation Level、Schedule Precision 和 Event Window；聚合网站或第三方 API 可以用于发现，但不得替代官方证据链接。

首版仅导入当前自然年剩余时间的事件，不做跨年度事件池或未来多年的规则展开；进入下一自然年时再执行年度刷新。

## 首版来源注册表

| 来源 | 官方入口 | 接入方式与频率 | 导入范围 | 默认字段 |
|---|---|---|---|---|
| OPM 美国联邦假日 | https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/ | 首次一次性录入或 CSV；年度刷新时同步一次 | 当前自然年剩余假日 | `Fixed` / `Date` / `factual` |
| BEA 发布时间表 | https://www.bea.gov/news/schedule | 抓取官方发布时间表；每日一次 | 当前自然年剩余发布 | `Confirmed`；精度以来源明确程度为准 |
| BLS 发布日历 | https://www.bls.gov/schedule/news_release/bls.ics | 下载并解析官方 iCalendar；每日一次 | 当前自然年剩余的 Employment Situation、CPI、PPI、JOLTS、ECI | `Confirmed`；精度以 iCalendar 为准 |
| FOMC 会议日历 | https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm | 抓取并解析当前年份会议日期；每日一次 | 当前自然年剩余会议 | `Confirmed` / `Date range` / `factual` |
| 人工导入 | 系统表单或 CSV | 提交后即时校验和写入 | 行业大会、品牌节点、特定人物行程等补漏事件 | 来源链接必填；默认 `Needs verification` / `internal_only` |

未来阶段：P1 为重点体育官方赛程与监管 Connector；P2 为企业 IR 观察与 SEC 确认。两者不属于首版开发范围。

## 连接器规则

- Connector 必须保存来源 URL、来源类型、最后核验时间、失效策略、原始解析字段和默认确认等级。
- 每次运行只处理 `[同步当日, 当年 12 月 31 日]` 内的事件；过期事件不新建，已有事件保留历史。
- BLS 使用官方 [iCalendar 订阅](https://www.bls.gov/schedule/news_release/bls.ics)；BEA 使用 [官方发布时间表](https://www.bea.gov/news/schedule)；FOMC 使用 [官方会议日历](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)；OPM 使用 [联邦假日表](https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/)。
- FOMC 未来会议只有日期行时，FOMC 会议模板可补充“货币政策会议”的类型说明；不能补写利率决定、会议结论、结果发布时间或不存在的链接。
- 连接器失败最多重试 3 次；失败显示来源异常，不得生成模拟事件。

## 大模型使用边界

- 程序获取官方数据、解析、校验、去重和写入；大模型不直接抓取后写库。
- 大模型仅接收已校验的结构化候选，完成标题标准化、分类、来源模板映射、已确认/未确认事实拆分和 Event Context Pack 补充。
- 任何大模型输出先经 schema 与原始字段一致性校验；日期、时间、主体和来源链接不能被模型改写。
- 大模型不得提升 Confirmation Level、补造 `Exact time`、猜测 FOMC 利率决定或其他未由来源支持的事实；必须忽略来源页面中的指令性文本。

## 不做

- 不做无边界的全网爬虫。
- 不将第三方聚合 API 当成权威事实来源。
- 不为每一个体育联盟或全部上市公司在首版建立 Connector。
