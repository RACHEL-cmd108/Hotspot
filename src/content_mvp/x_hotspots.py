from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import re
import sqlite3
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .twitterapi import TwitterAPIClient, TwitterAPIError, load_dotenv


REGIONS = {
    "worldwide": {"name": "Worldwide", "woeid": 1},
    "us": {"name": "United States", "woeid": 23424977},
    "uk": {"name": "United Kingdom", "woeid": 23424975},
    "jp": {"name": "Japan", "woeid": 23424856},
    "kr": {"name": "South Korea", "woeid": 23424868},
}

CATEGORY_RULES = [
    ("AI", (" ai ", "artificial intelligence", "openai", "chatgpt", "claude", "gemini", "人工智能", "生成式ai", "인공지능", "人工知能")),
    ("政治", ("election", "president", "congress", "parliament", "minister", "government", "trump", "biden", "政治", "选举", "总统", "政府", "대통령", "정부", "選挙", "首相")),
    ("科技", ("technology", "tech", "apple", "google", "microsoft", "tesla", "spacex", "iphone", "android", "科技", "芯片", "半导体", "テクノロジー", "기술")),
    ("商业/金融", ("market", "stock", "fed", "economy", "bank", "earnings", "finance", "经济", "股市", "金融", "央行", "경제", "金融")),
    ("加密", ("bitcoin", "ethereum", "crypto", "blockchain", "solana", "比特币", "以太坊", "加密", "仮想通貨", "暗号資産", "비트코인")),
    ("体育", ("football", "soccer", "baseball", "nba", "nfl", "mlb", "fifa", "match", "game", "体育", "比赛", "野球", "サッカー", "축구", "야구")),
    ("娱乐", ("movie", "music", "album", "actor", "actress", "anime", "concert", "娱乐", "电影", "音乐", "ドラマ", "映画", "アニメ", "연예", "영화")),
]


def classify(text: str) -> str:
    normalized = f" {text.casefold()} "
    for category, needles in CATEGORY_RULES:
        if any(needle in normalized for needle in needles):
            return category
    return "其他"


def _query_for_trend(trend: dict[str, Any]) -> str:
    target = trend.get("target")
    if isinstance(target, dict) and target.get("query"):
        return str(target["query"]).strip()
    return str(trend.get("name", "")).strip()


def collect_hotspots(client: TwitterAPIClient, count: int = 30, workers: int = 8) -> dict[str, Any]:
    regional: dict[str, list[dict[str, Any]]] = {}
    for region_id, region in REGIONS.items():
        regional[region_id] = client.get_trends(woeid=region["woeid"], count=count)

    queries = {
        _query_for_trend(trend)
        for trends in regional.values()
        for trend in trends
        if _query_for_trend(trend)
    }
    tweets: dict[str, dict[str, Any] | None] = {}

    def fetch(query: str) -> tuple[str, dict[str, Any] | None]:
        try:
            return query, client.get_top_tweet(query)
        except TwitterAPIError:
            return query, None

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        for query, tweet in executor.map(fetch, sorted(queries)):
            tweets[query] = tweet

    regions: list[dict[str, Any]] = []
    for region_id, region in REGIONS.items():
        items = []
        for trend in regional[region_id]:
            query = _query_for_trend(trend)
            tweet = tweets.get(query)
            combined = " ".join(
                [str(trend.get("name", "")), str(trend.get("meta_description", "")), str((tweet or {}).get("text", ""))]
            )
            items.append(
                {
                    "name": trend.get("name", query),
                    "query": query,
                    "rank": trend.get("rank"),
                    "meta_description": trend.get("meta_description"),
                    "category": classify(combined),
                    "representative_tweet": tweet,
                }
            )
        regions.append({"id": region_id, **region, "items": items})
    return {
        "source": "twitterapi.io",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tweet_selection": "Advanced Search / Top / first result",
        "regions": regions,
    }


def persist_to_trendradar(data: dict[str, Any], trendradar_root: Path) -> Path:
    """Persist the X snapshot into TrendRadar's native news schema plus tweet details."""
    now = datetime.now().astimezone()
    day = now.strftime("%Y-%m-%d")
    crawl_time = now.strftime("%H-%M")
    database = trendradar_root / "output" / "news" / f"{day}.db"
    database.parent.mkdir(parents=True, exist_ok=True)
    schema = (trendradar_root / "trendradar" / "storage" / "schema.sql").read_text(encoding="utf-8")
    with sqlite3.connect(database) as connection:
        connection.executescript(schema)
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS x_trend_details (
                news_item_id INTEGER PRIMARY KEY,
                region_id TEXT NOT NULL,
                region_name TEXT NOT NULL,
                query TEXT NOT NULL,
                category TEXT NOT NULL,
                meta_description TEXT,
                representative_tweet_json TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (news_item_id) REFERENCES news_items(id)
            );
            CREATE INDEX IF NOT EXISTS idx_x_trend_query ON x_trend_details(query);
            """
        )
        total = 0
        for region in data["regions"]:
            platform_id = f"x-{region['id']}"
            connection.execute(
                "INSERT INTO platforms(id, name, is_active, updated_at) VALUES (?, ?, 1, CURRENT_TIMESTAMP) "
                "ON CONFLICT(id) DO UPDATE SET name=excluded.name, is_active=1, updated_at=CURRENT_TIMESTAMP",
                (platform_id, f"X · {region['name']}"),
            )
            for item in region["items"]:
                tweet = item.get("representative_tweet") or {}
                url = tweet.get("url") or (
                    "https://x.com/search?q=" + urllib.parse.quote(item["query"]) + "&src=trend_click"
                )
                row = connection.execute(
                    "SELECT id, title FROM news_items WHERE url=? AND platform_id=?",
                    (url, platform_id),
                ).fetchone()
                if row:
                    item_id, old_title = row
                    if old_title != item["name"]:
                        connection.execute(
                            "INSERT INTO title_changes(news_item_id, old_title, new_title) VALUES (?, ?, ?)",
                            (item_id, old_title, item["name"]),
                        )
                    connection.execute(
                        "UPDATE news_items SET title=?, rank=?, last_crawl_time=?, "
                        "crawl_count=crawl_count+1, updated_at=CURRENT_TIMESTAMP WHERE id=?",
                        (item["name"], item["rank"], crawl_time, item_id),
                    )
                else:
                    cursor = connection.execute(
                        "INSERT INTO news_items(title, platform_id, rank, url, first_crawl_time, last_crawl_time) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (item["name"], platform_id, item["rank"], url, crawl_time, crawl_time),
                    )
                    item_id = cursor.lastrowid
                connection.execute(
                    "INSERT INTO rank_history(news_item_id, rank, crawl_time) VALUES (?, ?, ?)",
                    (item_id, item["rank"], crawl_time),
                )
                connection.execute(
                    """
                    INSERT INTO x_trend_details(
                        news_item_id, region_id, region_name, query, category,
                        meta_description, representative_tweet_json, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(news_item_id) DO UPDATE SET
                        region_id=excluded.region_id, region_name=excluded.region_name,
                        query=excluded.query, category=excluded.category,
                        meta_description=excluded.meta_description,
                        representative_tweet_json=excluded.representative_tweet_json,
                        updated_at=CURRENT_TIMESTAMP
                    """,
                    (
                        item_id, region["id"], region["name"], item["query"], item["category"],
                        item.get("meta_description"), json.dumps(tweet, ensure_ascii=False) if tweet else None,
                    ),
                )
                item["trendradar_item_id"] = item_id
                total += 1
        connection.execute(
            "INSERT INTO crawl_records(crawl_time, total_items) VALUES (?, ?) "
            "ON CONFLICT(crawl_time) DO UPDATE SET total_items=excluded.total_items",
            (crawl_time, total),
        )
        data["trendradar"] = {"database": str(database), "crawl_time": crawl_time, "item_count": total}
        connection.commit()
    return database


def render_dashboard(data: dict[str, Any]) -> str:
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>X 热点监控 · TrendRadar</title>
<style>
:root{{--bg:#f5f7fb;--card:#fff;--ink:#172033;--muted:#718096;--line:#e5e9f2;--blue:#2563eb}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:14px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
header{{background:#101827;color:white;padding:24px 32px}}header h1{{margin:0 0 6px;font-size:24px}}header p{{margin:0;color:#aeb9cc}}
.layout{{display:grid;grid-template-columns:190px 1fr;min-height:calc(100vh - 94px)}}aside{{padding:24px 16px;background:white;border-right:1px solid var(--line)}}
button{{font:inherit}}.filter{{display:block;width:100%;border:0;background:transparent;text-align:left;padding:10px 12px;border-radius:8px;color:#4a5568;cursor:pointer}}.filter.active{{background:#eaf1ff;color:var(--blue);font-weight:700}}
main{{padding:24px 30px}}.views,.regions{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}}.view,.region{{border:1px solid var(--line);background:white;padding:9px 14px;border-radius:99px;cursor:pointer}}.view.active,.region.active{{background:#172033;color:white;border-color:#172033}}
.summary{{display:flex;justify-content:space-between;align-items:end;margin-bottom:14px}}.summary h2{{margin:0;font-size:20px}}.summary span{{color:var(--muted)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px}}.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:17px;box-shadow:0 2px 8px #17203308}}
.top{{display:flex;gap:12px;align-items:start}}.rank{{font-size:22px;font-weight:800;color:#a0aec0;min-width:34px}}h3{{font-size:17px;margin:1px 0 7px}}.badge{{display:inline-block;background:#eef2f7;color:#526175;padding:3px 8px;border-radius:99px;font-size:12px}}
.tweet{{margin:14px 0 10px;line-height:1.55;white-space:pre-wrap;color:#344054}}.author,.metrics{{font-size:12px;color:var(--muted)}}.metrics{{margin-top:8px}}a{{color:var(--blue);text-decoration:none}}.empty{{color:var(--muted);font-style:italic}}
.event-card{{grid-column:span 1}}.event-meta{{display:flex;gap:8px;flex-wrap:wrap;margin:9px 0}}.section-title{{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin:15px 0 5px}}.list{{margin:5px 0;padding-left:18px;line-height:1.5}}.confidence{{color:#087a55;font-weight:700}}
@media(max-width:700px){{.layout{{grid-template-columns:1fr}}aside{{border-right:0;border-bottom:1px solid var(--line);padding:12px;display:flex;overflow:auto}}.filter{{width:auto;white-space:nowrap}}main{{padding:18px}}}}
</style></head><body>
<header><h1>𝕏 热点监控</h1><p>TrendRadar · Trending → Event Cluster → Event Card</p></header>
<div class="layout"><aside id="categories"></aside><main><div class="views" id="views"></div><div class="regions" id="regions"></div><div class="summary"><h2 id="heading"></h2><span id="updated"></span></div><div class="grid" id="grid"></div></main></div>
<script>const DATA={payload};let region='worldwide',category='全部',view='trends';
const cats=['全部','News','AI','政治','科技','商业/金融','加密','体育','娱乐','其他'];
function esc(s){{return String(s??'').replace(/[&<>\"']/g,m=>({{'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}}[m]))}}
function renderFilters(){{categories.innerHTML=cats.map(c=>`<button class="filter ${{c===category?'active':''}}" data-c="${{c}}">${{c}}</button>`).join('');categories.querySelectorAll('button').forEach(b=>b.onclick=()=>{{category=b.dataset.c;render()}})}}
function renderRegions(){{regions.innerHTML=DATA.regions.map(r=>`<button class="region ${{r.id===region?'active':''}}" data-r="${{r.id}}">${{r.name}}</button>`).join('');regions.querySelectorAll('button').forEach(b=>b.onclick=()=>{{region=b.dataset.r;render()}})}}
function renderViews(){{const complete=(DATA.event_clusters?.clusters||[]).filter(c=>c.event_card_complete).length,hasEvents=complete>0;views.innerHTML=`<button class="view ${{view==='trends'?'active':''}}" data-v="trends">趋势列表</button><button class="view ${{view==='events'?'active':''}}" data-v="events" ${{hasEvents?'':'disabled'}}>Event Cards (${{complete}})</button>`;views.querySelectorAll('button').forEach(b=>b.onclick=()=>{{if(!b.disabled){{view=b.dataset.v;render()}}}})}}
function isNews(x){{return ['AI','政治','科技','商业/金融','加密'].includes(x.category)}}
function list(xs){{return (xs||[]).map(x=>`<li>${{esc(typeof x==='string'?x:JSON.stringify(x))}}</li>`).join('')}}
function renderEvents(){{categories.style.display='none';regions.style.display='none';const all=DATA.event_clusters?.clusters||[],clusters=all.filter(c=>c.event_card_complete),pending=all.length-clusters.length;heading.textContent=`Event Cards (${{clusters.length}} 完整${{pending?` · ${{pending}} 待补全`:''}})`;grid.innerHTML=clusters.map(c=>{{const card=c.event_card||{{}},id=card.event_identity||{{}},facts=card.facts_and_evidence||{{}},life=card['生命周期']||{{}},opp=card['机会与风险']||{{}},angles=card['X内容的切入角度']||[];return `<article class="card event-card"><h3>${{esc(c.canonical_title||id.title)}}</h3><div class="event-meta"><span class="badge">${{esc(id.type||'其他')}}</span><span class="badge">${{c.members?.length||0}} 个趋势</span><span class="confidence">置信度 ${{Math.round((c.confidence||0)*100)}}%</span></div><div class="section-title">已确认事实</div><ul class="list">${{list(facts.confirmed_facts)}}</ul><div class="section-title">生命周期</div><div>${{esc(life.stage||'未知')}} · ${{esc(life.evidence||'')}}</div><div class="section-title">机会</div><ul class="list">${{list(opp.opportunities)}}</ul><div class="section-title">风险</div><ul class="list">${{list(opp.risks)}}</ul><div class="section-title">X 内容角度</div><ul class="list">${{list(angles.map(a=>a.hook||a.angle))}}</ul></article>`}}).join('')}}
function render(){{renderViews();updated.textContent=new Date(DATA.generated_at).toLocaleString();if(view==='events'){{renderEvents();return}}categories.style.display='block';regions.style.display='flex';renderFilters();renderRegions();const r=DATA.regions.find(x=>x.id===region);const items=r.items.filter(x=>category==='全部'||(category==='News'?isNews(x):x.category===category));heading.textContent=`${{r.name}} · ${{category}} (${{items.length}})`;grid.innerHTML=items.map(x=>{{const t=x.representative_tweet,a=t?.author||{{}};return `<article class="card"><div class="top"><div class="rank">${{esc(x.rank)}}</div><div><h3>${{esc(x.name)}}</h3><span class="badge">${{esc(x.category)}}</span></div></div>${{t?`<div class="tweet">${{esc(t.text)}}</div><div class="author">@${{esc(a.userName)}} · ${{esc(a.name)}}</div><div class="metrics">↻ ${{esc(t.retweetCount||0)}}　♡ ${{esc(t.likeCount||0)}}　◉ ${{esc(t.viewCount||0)}}　· <a href="${{esc(t.url)}}" target="_blank">查看原推</a></div>`:`<p class="empty">未找到可用的代表性推文</p>`}}</article>`}}).join('')}}render();</script></body></html>"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the TrendRadar X hotspot dashboard")
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--count", type=int, default=30)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--output-dir", type=Path, default=Path("TrendRadar/output/x-hotspots"))
    parser.add_argument("--trendradar-root", type=Path, default=Path("TrendRadar"))
    parser.add_argument("--render-existing", action="store_true")
    parser.add_argument("--persist-existing", action="store_true")
    parser.add_argument("--event-clusters", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    data_path = args.output_dir / "data.json"
    if args.render_existing:
        data = json.loads(data_path.read_text(encoding="utf-8"))
        if args.persist_existing:
            persist_to_trendradar(data, args.trendradar_root)
    else:
        load_dotenv(args.env_file)
        data = collect_hotspots(TwitterAPIClient(), count=args.count, workers=args.workers)
        persist_to_trendradar(data, args.trendradar_root)
    if args.event_clusters and args.event_clusters.is_file():
        data["event_clusters"] = json.loads(args.event_clusters.read_text(encoding="utf-8"))
    data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "index.html").write_text(render_dashboard(data), encoding="utf-8")
    print(args.output_dir / "index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
