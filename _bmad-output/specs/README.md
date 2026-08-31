# Hotspot Monitor SPEC 索引

本目录只保留当前有效的权威规则。阅读顺序如下：

| 顺序 | SPEC | 权威范围 |
|---:|---|---|
| 1 | [平台总规则](./spec-platform-rules/SPEC.md) | 全平台共同对象、Event 合同、内容链路、风险、发布、追踪与治理 |
| 2 | [主题圈雷达](./spec-topic-circle-radar/SPEC.md) | 主题圈账号、采集、同一事件识别、关注度指标与触发规则 |
| 3 | [未来事件运营排期](./spec-future-event-operations/SPEC.md) | 未来事件来源、证据、窗口、X Post Count、Action Score 与响应机制 |
| 4 | [热点内容生成 Skill](./spec-hotspot-content-generation-skill/SPEC.md) | 11 个账号技能包注册表、账号任务、三种响应模式与候选合同 |
| 5 | [跨来源事件合并](./spec-event-merge/SPEC.md) | 三来源独立触发后的语义匹配、合并评分、未合并路由、迟到来源与重复响应治理 |
| 6 | [Event 重复响应](./spec-event-repeat-response/SPEC.md) | 合格 Signal 的 24 小时多次响应窗口、五项增量条件、独立 Event 创建与响应基线 |
| 7 | [运营决策中心](./spec-operations-decision-center/SPEC.md) | 事件上下文的选题推荐准入、响应节奏、承接角度与人工采用边界 |

## 权威边界

- 平台共同规则只在“平台总规则”维护。
- 主题圈细则只在“主题圈雷达”维护。
- 未来事件细则只在“未来事件运营排期”维护。
- 内容生成 Skill 清单与职责只在“热点内容生成 Skill”维护。
- 跨来源 Event 的匹配、合并、未合并路由和晚合并规则只在“跨来源事件合并”维护。
- 同一事件发展线的 24 小时多次响应、增量指标和再次创建 Event 规则只在“Event 重复响应”维护。
- 运营决策中心的推荐准入、响应节奏、候选角度与人工采用边界只在“运营决策中心”维护。
- 专项 SPEC 与平台总规则冲突时：专项内部规则以专项 SPEC 为准，跨模块 Event、风险、发布和审计合同以平台总规则为准。

历史 Phase 0、重复解释稿和过渡性拆分文件已移至 `_bmad-output/archive/specs/`，不再作为当前实现依据。
