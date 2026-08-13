# 07 架构决策

权威决策在 [Architecture Spine](../../_bmad-output/planning-artifacts/architecture/architecture-热点监控-2026-08-11/ARCHITECTURE-SPINE.md)；本页提供开发索引。

| AD | 决定 |
| --- | --- |
| AD-1—2 | 模块化单体；Django 拥有 Web、领域、权限和 API。 |
| AD-3—6 | 99.5%/RTO/RPO、Google RBAC、数据最小化、审计与版本。 |
| AD-7—12 | 单一对象所有者、持久异步、AI 边界、PostgreSQL 权威、Outbox、托管可替换部署。 |
| AD-13 | 保留给未来外部写入的未知结果消歧；当前没有 Telegram 或自动 X 发帖。 |
| AD-14—16 | Event 实质变更复核下游、命令级授权、可回滚生产变更。 |
| AD-17 | 固定新版内容响应主链，移除旧 Opportunity/Task Plan/Telegram 实现对象。 |
| AD-18 | 活动策划与内容响应从 Event Card 独立分支；活动只生成三份方案，不自动执行。 |
| AD-19 | 账号、Content Skill 与规则均版本化；任务保存版本快照。 |
| AD-20 | Phase 0 对三个预配置 Predx X 账号分别建立任务；每个 Event × 账号至多一个任务，单账号异常不阻塞其他账号。 |

任何新信息若会改变这些决定或核心对象语义，必须先报告给产品负责人，由其决定是否同步修改上游 PRD/UX；架构不得自动回写上游。
