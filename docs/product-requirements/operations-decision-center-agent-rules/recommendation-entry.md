# 选题推荐准入与排序规则

## 1. 三条准入路径

### E1：公共关注度 `public_attention`

按 [public-attention.md](public-attention.md) 执行。第一期以 X 短时增速排行榜前 3 名为准。仅凭公共热度进入时使用 `attention_only`，不构造市场或产品连接。

### E2：实时市场承接 `live_market_match`

至少存在一个满足 [market-matching.md](market-matching.md) 中 `direct` 或 `related` 条件、状态可用且数据未过期的 PredX 市场时成立。

- `direct` 可自动成立；
- `related` 可成立但降低承接强度；
- `possible` 进入人工确认，不单独触发自动推荐；
- `none` 不成立。

### E3：产品价值承接 `product_value_match`

同时满足以下条件时成立：

1. 事件中存在有来源支持的具体研究对象：主体、动作、结果、条件、时间、证据或变化；
2. PredX 的产品定位、价值主张、用户场景或已上线能力中，至少一项能对该对象提供自然且具体的关联；不要求必须强绑定某个产品功能；
3. 能明确说明目标用户和用户价值；
4. 连接不依赖虚构市场、未上线能力或可替换到任意热点的泛化表述。

## 2. 准入决策

```text
IF public_attention = met
  RECOMMEND；没有承接方式时标记待人工探索
ELSE IF live_market_match = met
  RECOMMEND
ELSE IF product_value_match = met
  RECOMMEND
ELSE IF 任一路径 = uncertain
  REQUEST_REVIEW 或 REQUEST_CONTEXT
ELSE
  NOT_RECOMMENDED
```

## 3. 排序规则

先按 [response-urgency.md](response-urgency.md) 的三个可验证触发器区分 `immediate / today`，再在同一处理节奏内排序。

同层排序因素：

- 最新实质变化更近；
- 市场匹配更强且市场可用；
- 产品连接更具体；
- 用户价值更明确；
- 证据更成熟；
- 风险更低；
- 与近期已推荐角度重复度更低。

禁止将上述因素压缩成无法解释的单一综合分对用户展示。程序可内部排序，但界面必须显示主要排序依据。

公共关注度为 `uncertain` 时，不得据此准入或触发立即响应；如果另外两条路径成立，可按其依据继续判断。

## 4. 处理节奏

本子系统只输出 `immediate / today`。需要等待新信息的事件不进入“持续观察”；新信息出现后作为更新上下文重新提交。
