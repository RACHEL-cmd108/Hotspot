# 公共热度准入规则（MVP）

## 1. 业务定义

第一期只使用 X。热点情报中心已经完成帖子聚合、事件识别和增速排行；运营决策中心读取事件排名，不重复计算热度。

事件代表帖子位于当前可用的“短时增速排行榜”前 3 名时，`public_attention = met`。`captured_at` 用于记录证据取得时间，不作为公共热度的准入门槛。

公共热度只授予进入选题推荐的资格，不证明事实为真、存在 PredX 市场或具备产品价值。

## 2. Agent 输入

```yaml
public_attention_input:
  source: hotspot_intelligence_center
  platform: X
  growth_rank: integer|null
  captured_at: ISO-8601|null
  event_id: string|null
  evidence_refs: []
```

## 3. 判断步骤

1. 检查 `growth_rank`；
2. `growth_rank <= 3` → `met`；
3. `growth_rank > 3` → `not_met`；
4. 排名缺失 → `uncertain`。

完成条件：输出结果、排名、证据取得时间和一句可追溯解释。

人工或其他来源提交的上下文如果没有增速排名，公共热度为 `uncertain`，但仍继续运行实时市场和产品价值两条准入路径。

## 4. 承接边界

只有公共热度成立、实时市场和产品价值均不成立时，输出：

```yaml
recommendation_basis: public_attention
bridge_type: attention_only
angle_set_status: no_mature_angle
```

Agent可以说明需要验证的承接方向，不生成成熟产品角度。
