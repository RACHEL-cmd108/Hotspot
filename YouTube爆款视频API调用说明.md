# YouTube 爆款视频 API 调用说明

## 1. 目标

系统每天自动运行一次，从以下数据源获取候选视频，最终交付 **10 个不重复的 YouTube 视频链接**：

- 5 个美国地区 YouTube 官方热门视频
- 5 个指定关键词下近 7 天的高播放视频

最终交付字段：

```text
视频标题
视频链接
视频来源
```

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
5. 最终选出 5 个视频。

### 关键词组

1. 合并四个关键词的搜索结果。
2. 按 `items[].id.videoId` 去重。
3. 排除直播中和即将直播的视频。
4. 保留近 7 天发布的视频。
5. 接口已通过 `order=viewCount` 按播放量从高到低返回，优先选择排名靠前的视频。
6. 最终选出 5个视频。

### 最终合并

1. 合并官方热门组 5 条和关键词组 5 条。
2. 再次按视频 ID 去重。
3. 如果两组之间存在重复视频，从对应候选列表中顺延补充。
4. 最终必须得到 10 个不同的视频。

## 6. 生成视频链接

不需要额外调用 API，使用视频 ID 拼接链接：

```javascript
const videoUrl = `https://www.youtube.com/watch?v=${videoId}`;
```

其中：

- 官方热门接口的视频 ID：`item.id`
- 搜索接口的视频 ID：`item.id.videoId`

## 7. 每日输出格式

推荐保存为以下结构：

```json
{
  "date": "2026-08-18",
  "videos": [
    {
      "title": "视频标题",
      "url": "https://www.youtube.com/watch?v=VIDEO_ID",
      "source": "YouTube官方热门-科技"
    },
    {
      "title": "视频标题",
      "url": "https://www.youtube.com/watch?v=VIDEO_ID",
      "source": "关键词-Polymarket"
    }
  ]
}
```

要求：

- `videos` 数组最终正好包含 10 条。
- 每条必须包含 `title`、`url` 和 `source`。
- 任务部分失败时，应记录错误；只要仍有足够候选视频，就从其他候选结果顺延补齐 10 条。

## 8. 定时任务流程

每天执行一次：

```text
调用 3 次 videos.list 获取官方分类热门视频
→ 调用 4 次 search.list 获取关键词视频
→ 合并并去重
→ 官方热门组选择 5 条
→ 关键词组选择 5 条
→ 再次去重并补齐
→ 拼接视频链接
→ 保存并交付 10 条结果
```

## 9. 验收标准

- 定时任务每天只运行一次。
- 数据地区为美国，即 `regionCode=US`。
- 官方热门覆盖人物与博客、新闻与政治、科技三个分类。
- 关键词覆盖 Polymarket、web3、politics、prediction market。
- 关键词结果只取近 7 天发布的视频。
- 最终输出 10 个不同的 YouTube 视频链接。
- 用户端只需要展示视频标题、链接和来源。
- API Key 不出现在用户端、代码仓库或公开日志中。

## 10. 官方文档

- [YouTube Data API：videos.list](https://developers.google.com/youtube/v3/docs/videos/list)
- [YouTube Data API：search.list](https://developers.google.com/youtube/v3/docs/search/list)
