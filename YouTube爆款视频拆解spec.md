# YouTube 爆款视频拆解 Spec

## 1. 目标

系统每天自动运行一次，从以下数据源获取候选视频。系统先与历史视频库比对，只将当天首次入选的新视频交给下游拆解并推送；重复视频只更新持续火热状态，不重复拆解或推送。每天最多处理 10 个新视频：

- 5 个美国地区 YouTube 官方热门视频
- 5 个指定关键词下近 7 天的高播放视频

每条视频的基础字段：

```text
视频标题
视频链接
视频入选来源
```

“视频入选来源”指该视频通过哪条采集规则进入候选池，例如“YouTube 官方热门-科技”或“关键词-web3”。它不代表观众实际来自推荐、搜索还是订阅页面。

每条视频的最终分析只交付三个部分：

```text
主要原因
具体表现
复刻建议
```

复杂的视频分段、叙事分析和候选因素比较仅作为模型内部判断过程，不向用户展开。

## 2. API 准备

1. 登录 [Google Cloud 控制台](https://console.cloud.google.com/)。
2. 创建或选择一个 Google Cloud 项目。
3. 启用 [YouTube Data API v3](https://console.cloud.google.com/apis/library/youtube.googleapis.com)。
4. 在“API 和服务 → 凭据”中创建 API Key。
5. 将 API Key 配置在服务端环境变量中：

```env
YOUTUBE_API_KEY=你的API密钥
```

API Key 不得放在前端代码中，也不得提交到 Git 仓库。

API 基础地址：

```text
https://www.googleapis.com/youtube/v3
```

## 3. 获取美国官方热门视频

调用接口：

```http
GET https://www.googleapis.com/youtube/v3/videos
```

分别调用以下三个 YouTube 官方分类：

| 分类 | `videoCategoryId` |
|---|---:|
| 人物与博客 | `22` |
| 新闻与政治 | `25` |
| 科技 | `28` |

请求模板：

```http
GET https://www.googleapis.com/youtube/v3/videos
  ?part=snippet,statistics
  &chart=mostPopular
  &regionCode=US
  &videoCategoryId={CATEGORY_ID}
  &maxResults=10
  &key={YOUTUBE_API_KEY}
```

科技分类示例：

```text
https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=US&videoCategoryId=28&maxResults=10&key=YOUR_API_KEY
```

三个分类共返回最多 30 个候选视频。

处理要求：

- 保存返回结果中的 `id`，即视频 ID。
- 保存 `snippet.title`，即视频标题。
- 保留接口返回顺序，数组中的第一条视为该分类第 1 名。
- 排除 `snippet.liveBroadcastContent` 为 `live` 或 `upcoming` 的视频。

## 4. 获取关键词近 7 天高播放视频

调用接口：

```http
GET https://www.googleapis.com/youtube/v3/search
```

分别搜索以下四个关键词：

```text
Polymarket
web3
politics
prediction market
```

请求模板：

```http
GET https://www.googleapis.com/youtube/v3/search
  ?part=snippet
  &q={KEYWORD}
  &type=video
  &order=viewCount
  &publishedAfter={7天前的UTC时间}
  &regionCode=US
  &relevanceLanguage=en
  &maxResults=10
  &key={YOUTUBE_API_KEY}
```

`publishedAfter` 必须由程序每天动态计算：

```javascript
const publishedAfter = new Date(
  Date.now() - 7 * 24 * 60 * 60 * 1000
).toISOString();
```

Polymarket 请求示例：

```text
https://www.googleapis.com/youtube/v3/search?part=snippet&q=Polymarket&type=video&order=viewCount&publishedAfter=2026-08-11T00%3A00%3A00Z&regionCode=US&relevanceLanguage=en&maxResults=10&key=YOUR_API_KEY
```

注意：示例日期仅用于展示，实际调用时必须使用动态计算结果。

从返回结果中读取：

```text
items[].id.videoId
items[].snippet.title
items[].snippet.publishedAt
items[].snippet.liveBroadcastContent
```

四个关键词共返回最多 40 个候选视频。

## 5. 合并及筛选规则

### 官方热门组

1. 合并三个官方分类的候选视频。
2. 按视频 ID 去重。
3. 排除直播中和即将直播的视频。
4. 优先选择各分类中排名靠前的视频。
5. 跳过已经推送过的视频，从候选列表中顺延选择最多 5 个新视频。

### 关键词组

1. 合并四个关键词的搜索结果。
2. 按 `items[].id.videoId` 去重。
3. 排除直播中和即将直播的视频。
4. 保留近 7 天发布的视频。
5. 接口已通过 `order=viewCount` 按播放量从高到低返回，优先选择排名靠前的视频。
6. 跳过已经推送过的视频，从候选列表中顺延选择最多 5 个新视频。

### 最终合并

1. 合并官方热门组和关键词组的新视频。
2. 再次按视频 ID 去重。
3. 如果两组之间存在重复视频，从对应候选列表中顺延补充新视频。
4. 当天最多得到 10 个不同的新视频；没有足够新视频时允许少于 10 个，不得用历史视频补足数量。

### 跨日去重与持续火热

系统使用 `video_id` 作为跨日唯一键，维护持久化的视频历史库。每天抓取并完成当日基础过滤后，先与历史视频库比对：

- **历史视频**：已在历史库中存在。更新当天观察记录和持续火热天数，不进入拆解队列，不再次推送。
- **新视频**：历史库中不存在。完成当日筛选后写入历史库，并生成 `video_analysis_job` 交给下游 Agent。

历史记录至少包含：

```json
{
  "video_id": "VIDEO_ID",
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "title": "视频标题",
  "first_seen_date": "2026-08-21",
  "last_seen_date": "2026-08-21",
  "consecutive_hot_days": 1,
  "board_status": "active",
  "board_visible_until": "2026-08-27",
  "reappearance_count": 0,
  "last_reappearance_gap_days": null,
  "last_video_metrics": {
    "view_count": 1200000,
    "like_count": 68000,
    "comment_count": 3200
  },
  "selection_sources": [],
  "matched_keywords": ["web3", "prediction market"],
  "keyword_hit_count": 2,
  "discovery_labels": ["多关键词命中"],
  "pushed_at": "2026-08-21T12:00:00Z"
}
```

`consecutive_hot_days` 的更新规则：

1. 视频首次写入历史库时为 `1`。
2. 如果本次抓取日期是 `last_seen_date` 的下一自然日，则加 `1`。
3. 同一视频一天内命中多个分类或关键词，只计算一天。
4. 如果中间有一天未被当天候选结果捕获，之后再次出现时重置为 `1`。
5. “持续火热 N 天”只表示该视频连续 N 天仍出现在本系统每日抓取到的候选结果中，不等同于 YouTube 官方公布的连续热门天数。

### 七日滚动看板与再次上榜

看板每天刷新，展示最近 7 个自然日内被系统捕获的视频，而不是每周固定某一天才更新：

1. 每次捕获视频时，将 `board_status` 设为 `active`，并把 `board_visible_until` 更新为 `last_seen_date + 6 天`。
2. 到 `board_visible_until` 当天结束后仍未再次捕获，该视频退出看板，`board_status` 变为 `expired`；历史记录和既有拆解结果继续保留。
3. 如果历史视频在非连续日期再次被捕获，计算：

```text
再次上榜间隔天数 = 本次抓取日期 - 上次 last_seen_date
```

4. 为该视频增加动态标签 `N天后再次上榜`，更新 `last_reappearance_gap_days=N`，并将 `reappearance_count` 加 `1`。
5. 再次上榜后，`consecutive_hot_days` 重置为 `1`，`board_status` 恢复为 `active`，重新计算七日展示期限。
6. 如果视频已经退出看板，再次上榜时重新进入看板并复用已有拆解结果；不重新调用拆解 Agent，也不作为当天新视频重复推送。

示例：视频在 8 月 1 日最后一次被捕获，8 月 4 日再次出现，则添加 `3天后再次上榜` 标签：

```json
{
  "last_seen_date": "2026-08-04",
  "consecutive_hot_days": 1,
  "board_status": "active",
  "reappearance_count": 1,
  "last_reappearance_gap_days": 3,
  "discovery_labels": ["3天后再次上榜"]
}
```

### 多关键词命中标签

同一视频在同一天命中两个或更多不同的配置关键词时，增加 `多关键词命中` 标签：

```json
{
  "matched_keywords": ["web3", "prediction market"],
  "keyword_hit_count": 2,
  "discovery_labels": ["多关键词命中"]
}
```

计算规则：

1. 只统计 `keyword_search` 类型的入选来源，YouTube 官方热门分类不计入关键词数量。
2. 关键词先按系统配置的标准名称去重；同一关键词重复返回只计算一次。
3. `keyword_hit_count >= 2` 时添加 `多关键词命中` 标签，否则不添加。
4. 多关键词命中是当天的热度旁证，不增加额外的 `consecutive_hot_days`；一天仍只计算一天。
5. 历史视频再次出现时，更新当天的 `matched_keywords`、`keyword_hit_count` 和 `discovery_labels`，并保留可能存在的 `N天后再次上榜` 标签，但不重新推送。

历史视频再次出现时，应合并当天新增的 `selection_sources`，刷新 `last_video_metrics`、`last_seen_date`、看板状态和当天标签。历史记录更新不触发拆解 Agent，也不进入当天用户推送。

## 6. 生成视频链接

不需要额外调用 API，使用视频 ID 拼接链接：

```javascript
const videoUrl = `https://www.youtube.com/watch?v=${videoId}`;
```

其中：

- 官方热门接口的视频 ID：`item.id`
- 搜索接口的视频 ID：`item.id.videoId`

生成后必须验证 `video_url` 非空且符合 `https://www.youtube.com/watch?v={videoId}`。`video_url` 是拆解 Agent 定位和读取视频内容的必填字段；缺少有效链接的视频不得进入拆解队列。

## 7. 统一拆解任务对象

`videos.list` 和 `search.list` 的原始返回结构不同。两个来源完成合并、去重和数据补齐后，必须统一转换为 `video_analysis_job`，拆解 Agent 只接收这一种输入，不直接读取任何 YouTube API 原始响应。

```json
{
  "job_id": "youtube:VIDEO_ID:2026-08-21",
  "video_id": "VIDEO_ID",
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "title": "视频标题",
  "thumbnail_url": "https://i.ytimg.com/vi/VIDEO_ID/hqdefault.jpg",
  "published_at": "2026-08-21T10:00:00Z",
  "duration": "PT1M2S",
  "discovery": {
    "selection_sources": [
      {
        "type": "youtube_trending",
        "label": "YouTube官方热门-科技",
        "rank": 3
      },
      {
        "type": "keyword_search",
        "label": "关键词-web3",
        "rank": 2
      }
    ],
    "matched_keywords": ["web3"],
    "keyword_hit_count": 1,
    "discovery_labels": []
  },
  "video_metrics": {
    "view_count": 1200000,
    "like_count": 68000,
    "comment_count": 3200
  },
  "channel": {
    "channel_id": "CHANNEL_ID",
    "channel_title": "频道名称"
  }
}
```

### 字段规则

- `video_id`、`video_url`、`title` 和 `discovery.selection_sources` 为入队必填字段。
- `video_url` 是拆解 Agent 获取视频画面、字幕及页面信息的入口，必须保留到最终分析结果中。
- 同一视频通过多个渠道入选时，按 `video_id` 去重，但完整保留所有 `selection_sources`；同时从多个渠道入选可作为热度旁证。
- `discovery.matched_keywords` 保存当天命中的去重关键词；命中两个或更多关键词时，在 `discovery.discovery_labels` 中添加 `多关键词命中`。
- `search.list` 只负责发现候选视频。所有候选视频统一通过 `videos.list` 补齐详情和统计数据后再构造任务对象。
- 无法获取的非必填数据使用 `null` 或空数组，保持字段存在，不得虚构。

### 模块职责边界

上游采集模块只负责：

- 从官方热门与关键词搜索中发现候选视频；
- 合并、去重并选出 10 个视频；
- 生成并验证 `video_url`；
- 统一视频标题、入选来源及 API 已返回的基础统计信息；
- 输出 `video_analysis_job`。

下游拆解 Agent 负责：

- 通过 `video_url` 读取视频页面和视频内容；
- 获取或生成带时间戳字幕，提取必要画面证据；
- 调查频道订阅量及近期同类型视频表现，判断账号基本盘；
- 综合选题、包装、内容表现和账号因素完成爆款归因；
- 读取系统中当前启用的产品配置，生成产品二创建议。

上游不生成字幕、不提取视频帧，也不调查频道近期同类型视频。若下游无法访问链接且无法获得任何视频内容证据，任务标记为 `content_unavailable`，不得生成内容归因。

### 交接格式

采集模块向拆解 Agent 交付：

```json
{
  "date": "2026-08-21",
  "analysis_jobs": [
    {
      "video_id": "VIDEO_ID",
      "video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
      "title": "视频标题",
      "discovery": {
        "selection_sources": [
          {
            "type": "keyword_search",
            "label": "关键词-Polymarket",
            "rank": 1
          }
        ],
        "matched_keywords": ["Polymarket"],
        "keyword_hit_count": 1,
        "discovery_labels": []
      }
    }
  ]
}
```

`analysis_jobs` 只包含当天筛选出的新视频，最多 10 个不同的 `video_id`，且每个任务都有可访问的 `video_url`。如果当天没有新视频，允许提交空数组并生成“今日暂无新增视频”的运行结果。

## 8. 下游 Agent 的归因准备

上游交付 `video_analysis_job` 后，下游 Agent 通过 `video_url` 自行补齐：

```text
视频内容、带时间戳字幕和必要画面帧
标题、缩略图或 Shorts 首帧所表达的观看承诺
频道订阅量
频道近期同类型视频的播放量
```

由 `search.list` 获得的视频仍应由上游批量调用 `videos.list`，统一补齐当前视频的基础信息和统计数据：

```http
GET https://www.googleapis.com/youtube/v3/videos
  ?part=snippet,statistics,contentDetails
  &id={逗号分隔的视频ID}
  &key={YOUTUBE_API_KEY}
```

从结果中读取：

```text
snippet.channelId
snippet.publishedAt
snippet.thumbnails
statistics.viewCount
statistics.likeCount
statistics.commentCount
contentDetails.duration
```

下游 Agent 可使用 `channels.list` 获取公开订阅量：

```http
GET https://www.googleapis.com/youtube/v3/channels
  ?part=statistics
  &id={逗号分隔的频道ID}
  &key={YOUTUBE_API_KEY}
```

从结果中读取 `statistics.subscriberCount`，并继续调查该频道近期 10～20 条同类型视频。如果频道隐藏订阅量，则标记为未知，不得推算。

### 账号基本盘校正

官方热门或关键词高播放只说明视频已进入候选范围，不能解释视频为何获得流量。订阅量也只能辅助判断，不能直接代表视频的正常播放水平。下游 Agent 应对比该频道近期 10～20 条同类型视频，计算：

```text
账号突破倍数 = 当前视频播放量 ÷ 频道近期同类型视频播放量中位数
粉丝穿透率 = 当前视频播放量 ÷ 频道订阅量
传播速度 = 当前视频播放量 ÷ 发布后经过时间
```

`账号突破倍数` 是判断视频是否超出账号基本盘的主要公开指标。若缺少频道历史数据，只能说明“无法排除账号基本盘影响”，不得断言视频因内容而爆。

YouTube Data API 不提供公开的完播率、留存曲线、分享数和流量来源。没有频道后台数据时，模型只能判断潜在留存或传播机制，不能把它们写成已经验证的爆款原因。

## 9. 爆款视频拆解逻辑

模型内部综合判断以下五类因素：

1. **账号基本盘**：播放量是否明显超过该频道近期常态。
2. **选题吸引力**：具体讲了什么；击中了什么热点、情绪、需求、共鸣或信息差。
3. **流量包装**：标题、缩略图、首帧和开场是否形成清晰承诺。
4. **内容留存**：故事、信息、冲突、证据、反转或剪辑如何帮助观众继续观看。
5. **传播触发**：内容是否具有值得评论、分享、收藏或重播的观点、情绪或实用价值。

模型必须从中判断一个**第一流量驱动力**，并明确主次，例如：

```text
选题是主因，剪辑是放大器，账号基本盘提供冷启动。
```

“主要原因”不能只写“选题好”或“剪辑好”，必须写明：

- 具体选择了什么话题；
- 为什么这个话题吸引目标用户；
- 它具体击中了哪种情绪、需求、热点或信息差。

分析过程遵循以下证据规则：

- 区分可观察事实、合理解释和待验证假设。
- 无法读取音频时，不推断具体音乐、音效、语速或语气。
- 没有留存、分享或转化数据时，使用“可能帮助”而非确定性归因。
- 不因为视频播放量高，就把所有内容元素解释为成功原因。
- 复刻底层机制，不照搬原视频人物、文案、素材、Meme 或固定时间结构。

## 10. 最终产出物

每条视频保留 `video_url`，并只输出以下三个分析部分，不展示逐帧表格、完整时间轴或中间推理。

```text
【主要原因】

选题：用一句话写清视频具体讲了什么。
为什么吸引人：写清它击中的情绪、需求、热点、共鸣或信息差。
核心流量判断：明确第一流量驱动力，并说明账号基本盘是否足以解释当前播放量。

【具体表现】

关键手法：只写最关键的一到两个内容、叙事、包装或剪辑手法。
作用：说明这些手法如何放大选题、帮助理解、维持注意力或促进传播。

【复刻建议】

可复刻机制：提炼可迁移的底层选题或表达机制。
产品二创选题：结合我们的产品，给出一个可以直接创作的具体选题。
产品如何自然进入：说明产品从哪个问题、冲突或真实使用场景进入内容。
```

### 系统产品配置

产品信息由用户提前在系统内统一配置，不属于上游视频采集结果，也不随 `video_analysis_job` 重复传输。下游 Agent 在生成“产品二创选题”前，读取当前启用的产品配置，至少包括：

```text
产品是什么
目标用户是谁
解决什么问题
最有吸引力的能力
可以展示的真实场景或证据
禁止或无法证明的宣传内容
```

系统应为产品配置保存稳定的产品标识和配置版本。下游分析记录实际使用的 `product_profile_id` 与 `product_profile_version`，确保二创建议可以追溯到当时的产品资料。

当前没有启用的产品配置，或配置缺少关键能力、目标用户和禁用声明时，保留“可复刻机制”，将“产品二创选题”和“产品如何自然进入”标记为待补充，不得虚构产品能力。

### 产出质量要求

- 结论短、明确、可执行，主因只能有一个。
- 具体表现只保留一到两个真正关键的放大因素。
- 产品二创必须是具体选题，而不是“结合产品做内容”一类空泛建议。
- 产品应作为原选题中问题、冲突或需求的自然回应，避免生硬插入广告。
- 若缺少频道历史数据、留存或流量来源，应简短说明置信度限制。

## 11. 每日输出格式

推荐保存为以下结构：

```json
{
  "date": "2026-08-18",
  "new_videos": [
    {
      "title": "视频标题",
      "url": "https://www.youtube.com/watch?v=VIDEO_ID",
      "selection_sources": [
        {
          "type": "youtube_trending",
          "label": "YouTube官方热门-科技",
          "rank": 3
        }
      ],
      "matched_keywords": [],
      "keyword_hit_count": 0,
      "discovery_labels": [],
      "analysis": {
        "main_reason": {
          "topic": "视频的具体选题",
          "why_attractive": "选题吸引用户的原因",
          "traffic_judgment": "第一流量驱动力及账号因素判断"
        },
        "execution": {
          "key_technique": "最关键的一到两个手法",
          "effect": "手法起到的作用"
        },
        "replication": {
          "reusable_mechanism": "可迁移的底层机制",
          "product_remix_topic": "结合产品的具体二创选题",
          "product_entry": "产品自然进入内容的方式"
        }
      }
    }
  ]
}
```

要求：

- `new_videos` 只包含当天首次入选并完成拆解的新视频，数量为 0～10 条。
- 每条必须包含 `title`、`url`、`selection_sources` 和 `analysis`。
- `selection_sources` 必须从对应 `video_analysis_job.discovery.selection_sources` 原样保留。
- `matched_keywords`、`keyword_hit_count` 和 `discovery_labels` 必须从对应 `video_analysis_job.discovery` 原样保留；多关键词命中时向用户显示“多关键词命中”。
- 最终结果中的 `url` 必须与对应 `video_analysis_job.video_url` 完全一致。
- `analysis` 必须对应“主要原因、具体表现、复刻建议”三个部分。
- 重复视频不进入 `new_videos`，只更新历史库中的 `consecutive_hot_days` 等状态。
- 任务部分失败时应记录错误，并在候选列表中顺延选择其他新视频；不得用已经推送过的视频补足数量。

## 12. 定时任务流程

每天执行一次：

```text
调用 3 次 videos.list 获取官方分类热门视频
→ 调用 4 次 search.list 获取关键词视频
→ 合并并去重
→ 汇总每条视频当天命中的不同关键词并生成多关键词命中标签
→ 与历史视频库按 video_id 比对
→ 为连续出现的视频更新持续火热天数、最新指标和入选来源
→ 为非连续出现的历史视频生成“X天后再次上榜”标签并恢复看板展示
→ 移除超过七日展示期限且未再次出现的视频卡片，但保留历史记录
→ 从未推送的新视频中选择官方热门组最多 5 条
→ 从未推送的新视频中选择关键词组最多 5 条
→ 再次去重；不足 10 条时不使用历史视频补齐
→ 为每条视频生成并验证 video_url
→ 补充当前视频的基础信息和统计数据
→ 将新视频写入历史库并标准化为 0～10 个 video_analysis_job
→ 将统一任务对象交给拆解 Agent
→ Agent 通过 video_url 读取视频并生成带时间戳字幕和画面证据
→ Agent 调查频道订阅量及近期同类型视频表现
→ 判断第一流量驱动力
→ Agent 读取系统中当前启用的产品配置
→ 生成产品二创建议
→ 只保存并推送当天新增视频的三段式分析结果
```

## 13. 验收标准

- 定时任务每天只运行一次。
- 数据地区为美国，即 `regionCode=US`。
- 官方热门覆盖人物与博客、新闻与政治、科技三个分类。
- 关键词覆盖 Polymarket、web3、politics、prediction market。
- 关键词结果只取近 7 天发布的视频。
- 每天最多推送 10 个不同的新视频链接；没有足够新视频时允许少于 10 个。
- 系统按 `video_id` 维护持久化历史库，滚动 7 天窗口造成的重复视频不会被再次拆解或推送。
- 重复视频会更新 `last_seen_date`、`consecutive_hot_days`、最新指标和入选来源。
- `consecutive_hot_days` 只在连续自然日被候选结果捕获时增加，同一天多来源入选只计算一次，中断后重置为 1。
- 同一天命中两个或更多不同关键词时添加“多关键词命中”标签，但持续火热天数仍只增加 1。
- 看板按日刷新并采用七日滚动展示；超过七日未被再次捕获的视频退出看板，但历史记录和拆解结果保留。
- 历史视频在非连续日期再次出现时显示“X天后再次上榜”，重新进入看板，但不重新拆解或重复推送。
- 两个采集来源已统一转换为 `video_analysis_job`，拆解 Agent 不接收 API 原始响应。
- 每个拆解任务均包含非空且格式有效的 `video_id`、`video_url`、`title` 和 `selection_sources`。
- 同一视频从多个渠道入选时，各入选来源被合并保留，而不是覆盖或重复入队。
- `analysis_jobs` 只包含当天新增视频，数量为 0～10 个，且每个任务的有效链接已交付给拆解 Agent。
- 当天推送结果不包含已经推送过的历史视频。
- 上游未承担字幕生成、视频帧提取或频道历史基准调查。
- 下游 Agent 已通过 `video_url` 获取视频内容和带时间戳字幕，或明确标记 `content_unavailable`。
- 每条视频只向用户展示“主要原因、具体表现、复刻建议”。
- “主要原因”必须写明具体选题及其吸引用户的原因，并给出唯一主因。
- “具体表现”最多保留一到两个关键放大手法。
- “复刻建议”必须包含可复刻机制、具体产品二创选题和产品自然进入方式。
- 产品二创建议来自系统当前启用的产品配置，并记录所用的产品标识和配置版本。
- 下游 Agent 已使用频道近期同类型视频校正账号基本盘；无法获取时明确标记数据缺失。
- 没有留存、分享或流量来源数据时，不作确定性效果归因。
- API Key 不出现在用户端、代码仓库或公开日志中。

## 14. 官方文档

- [YouTube Data API：videos.list](https://developers.google.com/youtube/v3/docs/videos/list)
- [YouTube Data API：search.list](https://developers.google.com/youtube/v3/docs/search/list)
- [YouTube Data API：channels.list](https://developers.google.com/youtube/v3/docs/channels/list)
