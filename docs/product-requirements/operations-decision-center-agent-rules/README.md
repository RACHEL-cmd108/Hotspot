# 运营决策中心 Agent 规则包

状态：设计草案 v0.1  
更新：2026-08-28

> 当前第一期的业务交付以 [运营决策中心 MVP 规则](../../../_bmad-output/specs/spec-operations-decision-center/SPEC.md) 为准。本目录内文件是给开发与 Agent 进一步落地时按需查阅的细则，不需要在当前产品定义阶段逐份确认。

## 目的

本规则包定义运营决策中心如何把任意来源的事件上下文转化为 PredX 产品选题推荐与候选承接角度。它从以下输入开始：

- 已取得的 PredX 产品事实与能力边界；
- 已取得的 PredX 实时市场接口数据；
- 本次事件描述或事件上下文。

它结束于可解释、可追溯的选题判断与角度集合，不生成最终文案、脚本、素材、发布任务或下游交付动作。

> 本规则包反映 2026-08-28 之后的新设计方向。它与 2026-08-24 旧版运营决策中心 PRD 并行，冲突处不得静默合并；正式实施前由产品负责人确认基线。

## Agent 主流程

### 1. 理解输入

读取事件上下文、产品事实和实时市场。人工输入允许非结构化；只在缺失信息可能改变准入、市场匹配、风险或时效结论时请求补充。

完成条件：形成 `event_summary`、输入版本、来源状态、热度状态及关键缺口；无法形成事件描述时返回 `insufficient_context`。

### 2. 运行三条准入路径

按 [recommendation-entry.md](recommendation-entry.md) 分别检查：

1. `public_attention`：达到可验证的公共关注度准入；
2. `live_market_match`：存在有效的开放市场匹配；
3. `product_value_match`：存在自然、具体的产品价值连接。

三条路径可同时成立。任意一条成立即可进入选题推荐；均不成立则不推荐。

完成条件：每条路径都有 `met / not_met / uncertain` 结果、依据和使用的数据时间。

### 3. 形成产品承接判断

市场匹配调用 [market-matching.md](market-matching.md)。产品价值连接使用 [angle-space.md](angle-space.md) 中的产品价值承接面。仅有公共关注度成立、尚无承接方式时，输出 `attention_only`，不构造产品关联。

完成条件：承接类型为 `market / product_value / attention_only / none`，并能追溯到市场、产品事实或公共关注度依据。

### 4. 探索候选角度

仅对已进入推荐的事件生成候选角度。使用 [angle-space.md](angle-space.md) 探索不同承接面；角度数量由自然成立的方向决定，不为凑数生成。默认展示前 5 个，保留全部通过质量门的候选。

完成条件：每个角度都有核心主张、承接对象、目标用户、用户价值、成立依据、成熟度和风险；候选之间存在实质差异。

### 5. 运行质量门

按 [angle-quality.md](angle-quality.md) 检查每个候选。未通过硬门的候选不进入推荐集合；信息可补齐的候选可保留为 `needs_data`；有潜力但尚不成熟的候选标记为 `exploratory`。

完成条件：每个保留或淘汰的候选都有逐项质量结果与淘汰原因。

### 6. 判断响应节奏并输出

按 [response-urgency.md](response-urgency.md) 判断 `immediate / today`。立即响应仅由已定义的排行榜、12 小时内关键节点或 2 小时内关键事实三类可验证触发器决定。输出遵循 [output-contract.yaml](output-contract.yaml)。

完成条件：输出能解释“为什么进入、由什么承接、为什么是现在、有哪些角度、哪里不确定”。

### 7. 处理人工反馈与重新推荐

用户要求换角度、补充角度或重新推荐时，按 [regeneration-feedback.md](regeneration-feedback.md) 执行。默认只影响当前事件；长期偏好必须由用户明确保存。

完成条件：保留用户指定候选，不重复被否定的核心主张，产生新版本并记录相对上一版的变化。

## 参考文件路由

- 判断能否进入选题推荐或确定排序：读取 [recommendation-entry.md](recommendation-entry.md)。
- 判断公共关注度是否足以单独准入、解释热度阶段：读取 [public-attention.md](public-attention.md)。
- 判断立即响应或今日处理：读取 [response-urgency.md](response-urgency.md)。
- 匹配、排序或解释 PredX 实时市场：读取 [market-matching.md](market-matching.md)。
- 探索承接面和生成候选角度：读取 [angle-space.md](angle-space.md)。
- 评审角度是否合格、重复或硬蹭：读取 [angle-quality.md](angle-quality.md)。
- 处理保留、否定、替换、重新推荐和偏好范围：读取 [regeneration-feedback.md](regeneration-feedback.md)。
- 生成系统结果：遵循 [output-contract.yaml](output-contract.yaml)。
- 校准规则或验收实现：读取 [examples.md](examples.md)。
- 查看本轮一致性检查、已修正问题和发布缺口：读取 [SELF-REVIEW.md](SELF-REVIEW.md)。
- 校验公共关注度规则是否能被 Agent 唯一执行：读取 [public-attention-self-check.md](public-attention-self-check.md)。

## 权限边界

- Agent：默认研判、市场匹配建议、产品价值判断、角度探索、质量检查和重新推荐。
- 程序：实时数据获取、确定性阈值、版本、去重、状态流转、审计和权限门禁。
- 人工：规则发布、疑似市场匹配确认、高风险复核、判断推翻、角度修改及长期偏好授权。

低置信度、高风险、市场规则冲突、关键信息缺失或 `possible` 市场匹配进入人工复核，不静默自动确认。
