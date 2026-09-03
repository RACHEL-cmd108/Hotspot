# 响应节奏规则（MVP）

响应节奏回答“什么时候处理”，不回答“为什么值得进入选题推荐”。只有已准入事件才运行本规则。

## 1. 输出

```yaml
response_urgency:
  handling: immediate | today
  trigger_id: URG-01 | URG-02 | URG-03 | null
  evidence: []
  rationale: string
  recommended_review_deadline: ISO-8601|string
```

## 2. `immediate` 触发条件

只有命中以下任一项并提供对应证据时，才能输出 `immediate`：

- `URG-01 growth_top_3`：事件位于当前可用的 X 短时增速排行榜前 3 名；证据为排名和证据取得时间。
- `URG-02 milestone_within_12h`：与事件直接相关的发布、投票、结算、截止或正式决定将在未来 12 小时内发生；证据为节点和发生时间。
- `URG-03 material_fact_within_2h`：过去 2 小时内出现官方确认、正式结果或关键决定，并且该事实直接匹配开放的 PredX 市场或直接影响 PredX 产品；证据为事实、发生时间和连接对象。

程序负责排名新鲜度和时间差计算；Agent负责判断节点或新事实是否与当前事件、市场或产品直接相关。

立即响应的运营目标为“建议 2 小时内完成人工判断”。不得使用“机会窗口正在关闭”“事件很重要”或“建议尽快”等抽象理由触发立即响应。

## 3. `today`

事件已准入但未命中 URG-01、URG-02 或 URG-03 时输出 `today`，要求当天完成人工判断。

本子系统不输出“持续观察”；需要新信息后，由上下文收件箱接收更新并重新判断。
