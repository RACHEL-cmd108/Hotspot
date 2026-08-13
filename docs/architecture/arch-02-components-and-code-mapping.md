# 02 组件与代码映射

```mermaid
sequenceDiagram
  participant X as X API
  participant M1 as Discovery
  participant M2 as Event Intelligence
  participant M4 as Content Response
  participant AI as AI
  participant U as 运营人员
  X->>M1: 每小时地区趋势/详情来源
  M1->>M2: candidate_event.qualified.v1
  M2->>M4: event.response_rule_matched.v1
  M4->>M4: 对 3 个预配置账号逐一创建/标记异常
  M4->>AI: 每个可用账号生成 >=3 条专属候选
  AI-->>M4: 候选/失败
  U->>M4: 选择、调整、回填 X URL/失败原因
  M4->>M5: publication.recorded.v1
```

```text
src/hotspot_monitor/apps/
  shared/              # authz, audit, config_versions, outbox
  discovery/           # X polling, source snapshots, candidate events
  event_intelligence/  # Event/Fact/Evidence and Event Card projections
  campaign_planning/   # recommendations, cases, exactly-three proposals
  content_response/    # accounts, skills, ARTs, candidates, publications
  outcome_learning/    # performance, evaluation, proposals
  integrations/        # ports + X/AI/Google adapters
```

浏览器仅调用 Django 应用服务。同步命令只校验、写权威状态、审计和 Outbox；Worker 消费 Outbox 后采集 X、调用 AI 或刷新效果。每个 Worker 命令使用持久幂等键；失败留在可见队列，可重试或人工接管。
