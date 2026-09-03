# 重新推荐与反馈规则

## 1. 最终运营结果

| 结果 | 定义 | 指标归属 |
|---|---|---|
| `directly_adopted` | 运营选择 Agent 候选角度并原样采用。 | 选题采用、Agent 角度采用、首轮采用按是否重推计算。 |
| `adopted_after_edit` | 运营以某个 Agent 候选为基础，修改后形成最终角度。 | 选题采用、Agent 角度采用、修改后采用。 |
| `replaced_by_human` | 运营认可该选题，但放弃 Agent 候选，填写全新的人工角度。 | 选题采用；不计 Agent 角度采用。 |
| `not_adopted` | 运营决定本次不做该选题，或没有任何可用承接角度。 | 选题不采用、Agent 角度不采用。 |

第一期不通过文本相似度自动判断“修改”还是“人工新角度”，以运营人员选择的动作作为结果。

### “修改后采用”的含义

运营人员先选择一个 Agent 候选角度，再编辑并保存最终角度，即为 `adopted_after_edit`。它表达“Agent给出了可用起点，但需要人工调整”，不要求系统计算改动字数。

如果运营人员认为最终方向已经不再基于任何候选，应使用 `replaced_by_human`，而不是“修改后采用”。

## 2. 支持的中间动作

- `keep`：保留候选；
- `edit`：人工修改候选并生成新版本；
- `replace_one`：仅替换一个候选；
- `regenerate_unkept`：保留已选候选，替换其余候选；
- `regenerate_all`：生成全新集合；
- `add_human_angle`：补充人工角度并进入同一质量检查；
- `mark_not_applicable`：标记该方向不适用。

`regenerate_*` 是中间动作，不计入最终采用或不采用；一次判断最终必须落到四种运营结果之一。

## 3. 反馈原因

```yaml
too_generic: 角度太泛
weak_product_connection: 产品连接弱或硬蹭
incorrect_market_match: 市场匹配或结算语义错误
too_close_to_copy: 太像最终标题或具体文案
duplicate: 与其他候选实质重复
unclear_user_value: 用户价值不明确
insufficient_evidence: 证据或数据不足
too_risky: 风险过高
wrong_audience: 目标用户不合适
wrong_goal: 不符合当前运营目标
stale_timing: 时机已过
need_different_family: 希望探索不同承接面
other: 附自由文本说明
```

偏好反馈与质量纠错分开：`incorrect_market_match`、事实/证据错误、风险漏判属于质量纠错；其他通常属于偏好反馈。

## 4. 重新推荐步骤

1. 读取当前 Angle Set、已保留候选、被否定候选、反馈原因和自由文本要求。
2. 将否定理由转为当前事件的约束；只有用户明确授权时写入长期偏好。
3. 确定尚未覆盖且自然成立的承接面。
4. 生成替代候选并运行完整质量门。
5. 与当前和历史候选做语义去重。
6. 输出新版本及 `change_summary`。

完成条件：所有 `keep` 候选仍存在；被否定核心主张未换句话返回；新候选通过质量门；版本与差异可追溯。

## 5. 反馈作用范围

```yaml
current_event: 默认；仅约束当前事件后续生成
current_session: 仅约束本轮探索，结束后失效
project_preference: 用户明确保存后影响未来事件
quality_correction: 进入复核，不直接修改长期规则
```

少量反馈不得自动改写准入、市场匹配、产品事实或风险规则。长期规则变更必须版本化发布，只影响后续判断；历史结果保留原规则版本。

## 6. 采用率口径

```text
选题采用率
= (directly_adopted + adopted_after_edit + replaced_by_human) 的已审核选题数
÷ 已审核选题数

Agent角度采用率
= (directly_adopted + adopted_after_edit) 的已审核选题数
÷ 已审核选题数

首轮采用率
= 未发生重新推荐且结果为 directly_adopted 的选题数
÷ 已审核选题数

重推挽回率
= 发生重新推荐后最终 directly_adopted 或 adopted_after_edit 的选题数
÷ 发生过重新推荐的选题数
```

待审核推荐不进入任何采用率分母。

## 7. 版本要求

每次生成保存：

- `angle_set_version`；
- 来源事件、产品资料和市场快照版本；
- 生成时间；
- 触发动作；
- 保留、替换和新增的 Angle ID；
- 反馈原因和作用范围；
- `change_summary`；
- 操作者或 Agent 版本。
