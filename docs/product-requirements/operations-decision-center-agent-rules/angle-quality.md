# 承接角度质量规则

## 1. 硬门

任一硬门失败，Angle 不进入推荐集合。

| Gate | 通过条件 |
|---|---|
| Q1 具体承接 | 指向真实市场，或清楚说明与 PredX 产品定位、价值主张、用户场景或产品能力的关联。 |
| Q2 核心主张 | 用一句可检验的切入主张说明从哪里切入。 |
| Q3 用户价值 | 明确目标用户及其获得的理解、判断或研究价值。 |
| Q4 依据 | 核心主张能追溯到事件证据、市场快照或产品事实。 |
| Q5 时效 | 说明为什么现在成立；长期价值则说明使用窗口。 |
| Q6 边界 | 区分事实、市场状态、推断和未知，不越过产品与风险边界。 |
| Q7 非文案 | 输出承接主张而非完整标题、帖子、大纲或脚本。 |

## 2. 质量维度

每项使用离散值，不只输出不可解释的总分。

```yaml
product_connection: strong | moderate | weak
user_value: clear | partial | unclear
evidence_readiness: ready | needs_data | unsupported
timeliness: immediate | current | evergreen | expired
distinctiveness: distinct | overlapping | duplicate
risk: low | medium | high | blocked
maturity: ready | needs_data | exploratory | rejected
```

映射规则：

- `unsupported`、`duplicate`、`expired` 或 `blocked` → `rejected`；
- 方向成立但缺少可取得数据 → `needs_data`；
- 高热场景下连接仍待验证 → `exploratory`；
- 所有硬门通过且风险可控 → `ready`。

## 3. 重复判断

两个候选若承接对象、核心机制、核心主张和用户价值基本相同，即使措辞不同也视为重复。重复候选保留依据更强、表达更清楚的一条。

以下不是有效差异：

- 只替换疑问句和陈述句；
- 只改“如何、为什么、哪些”；
- 只改内容形式或标题风格；
- 使用相同市场和证据得出相同主张。

## 4. 硬蹭识别

出现以下任一情况，产品连接判为 `weak` 或候选拒绝：

- 产品名或 CTA 可删除而不影响主张；
- 产品连接可以原样替换到任意热点；
- 只有品牌曝光，没有新增用户价值；
- 需要虚构市场、概率、合作或未上线能力；
- 以“任何事情都可预测”作为唯一理由；
- 热度被当作产品关联证据。

## 5. Angle 必备字段

```yaml
angle_id:
angle_family:
core_claim:
bridge_type: market | product_value
bridge_object:
event_stage:
target_user:
user_value:
operational_goal:
supporting_evidence_ids: []
market_snapshot_refs: []
required_data: []
quality: {}
risk_notes: []
```

`recommended_content_question` 可作为界面示意字段，但必须标记为非最终文案，不作为 Angle 的唯一内容。
