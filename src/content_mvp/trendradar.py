from __future__ import annotations

import re
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import AccountProfile, ActionPackage


SOURCE_RELIABILITY = {
    "财联社热门": 88,
    "华尔街见闻": 86,
    "澎湃新闻": 84,
    "凤凰网": 78,
    "百度热搜": 68,
    "今日头条": 66,
    "知乎": 62,
    "微博": 60,
    "抖音": 56,
    "bilibili 热搜": 54,
    "贴吧": 45,
}


@dataclass(frozen=True)
class TrendCandidate:
    item_id: int
    title: str
    platform_id: str
    platform_name: str
    rank: int
    url: str
    first_crawl_time: str
    last_crawl_time: str
    crawl_count: int
    best_rank: int
    previous_rank: int | None
    cluster_size: int = 1


class TrendRadarAdapter:
    def __init__(self, trendradar_root: Path) -> None:
        self.root = trendradar_root

    def latest_news_db(self) -> Path:
        databases = sorted((self.root / "output" / "news").glob("????-??-??.db"))
        if not databases:
            raise FileNotFoundError(f"no TrendRadar news database in {self.root / 'output/news'}")
        return databases[-1]

    def read_candidates(self, limit: int = 50) -> tuple[Path, list[TrendCandidate]]:
        database = self.latest_news_db()
        uri = f"file:{database.resolve()}?mode=ro"
        with sqlite3.connect(uri, uri=True) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT n.id AS item_id, n.title, n.platform_id, p.name AS platform_name,
                       n.rank, n.url, n.first_crawl_time, n.last_crawl_time,
                       n.crawl_count, MIN(h.rank) AS best_rank,
                       (SELECT h2.rank FROM rank_history h2
                        WHERE h2.news_item_id = n.id
                        ORDER BY h2.id DESC LIMIT 1 OFFSET 1) AS previous_rank
                FROM news_items n
                JOIN platforms p ON p.id = n.platform_id
                LEFT JOIN rank_history h ON h.news_item_id = n.id
                WHERE n.url != ''
                GROUP BY n.id
                ORDER BY n.rank ASC, n.crawl_count DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        candidates = [TrendCandidate(**dict(row)) for row in rows]
        return database, self._add_cluster_sizes(candidates)

    def to_action_package(
        self, candidate: TrendCandidate, account: AccountProfile, database: Path
    ) -> ActionPackage:
        audience_fit = self._audience_fit(candidate.title, account.interest_keywords)
        heat = {
            "source_reliability": float(SOURCE_RELIABILITY.get(candidate.platform_name, 60)),
            "freshness": self._freshness(database, candidate.last_crawl_time),
            "velocity": self._velocity(candidate),
            "audience_fit": audience_fit,
        }
        event_id = f"trendradar_{database.stem}_{candidate.platform_id}_{candidate.item_id}"
        return ActionPackage.from_dict(
            {
                "mode": "trend_capture",
                "event_id": event_id,
                "event_title": candidate.title,
                "verified_facts": [f"{candidate.platform_name} reports: {candidate.title}"],
                "source_urls": [candidate.url],
                "action_window": "breaking" if heat["freshness"] >= 80 else "developing",
                "objective": "hotspot_capture",
                "audience": account.audience,
                "participation_reason": "Watch for confirmation from a primary source and the next material development",
                "risks": ["TrendRadar headline is a signal, not independent fact verification"],
                "prohibited_claims": ["confirmed by Predx", "exclusive"],
                "markets": [],
                "relevance": {},
                "heat": heat,
            }
        )

    @staticmethod
    def candidate_metadata(candidate: TrendCandidate) -> dict[str, Any]:
        return asdict(candidate)

    @staticmethod
    def _audience_fit(title: str, keywords: list[str]) -> float:
        if not keywords:
            return 60.0
        normalized = title.casefold()
        matches = sum(1 for keyword in keywords if keyword.casefold() in normalized)
        if not matches:
            return 25.0
        return min(100.0, 70.0 + (matches - 1) * 10.0)

    @staticmethod
    def _freshness(database: Path, last_crawl_time: str) -> float:
        try:
            observed = datetime.strptime(f"{database.stem} {last_crawl_time}", "%Y-%m-%d %H-%M")
            age_hours = max(0.0, (datetime.now() - observed).total_seconds() / 3600)
        except ValueError:
            return 70.0
        if age_hours <= 2:
            return 100.0
        if age_hours <= 6:
            return 90.0
        if age_hours <= 12:
            return 80.0
        if age_hours <= 24:
            return 65.0
        return 35.0

    @staticmethod
    def _velocity(candidate: TrendCandidate) -> float:
        rank_signal = max(20.0, 100.0 - (candidate.rank - 1) * 4.0)
        cluster_bonus = min(15.0, (candidate.cluster_size - 1) * 5.0)
        if candidate.previous_rank is None:
            return min(100.0, rank_signal * 0.85 + cluster_bonus)
        movement = candidate.previous_rank - candidate.rank
        movement_signal = max(0.0, min(20.0, movement * 3.0))
        persistence = min(10.0, max(0, candidate.crawl_count - 1) * 2.0)
        return min(100.0, rank_signal * 0.7 + movement_signal + persistence + cluster_bonus)

    @classmethod
    def _add_cluster_sizes(cls, candidates: list[TrendCandidate]) -> list[TrendCandidate]:
        tokens = [cls._tokens(item.title) for item in candidates]
        sizes = []
        for index, left in enumerate(tokens):
            size = 1
            for other_index, right in enumerate(tokens):
                if index == other_index or not left or not right:
                    continue
                overlap = len(left & right) / max(1, min(len(left), len(right)))
                if overlap >= 0.5:
                    size += 1
            sizes.append(size)
        return [TrendCandidate(**{**asdict(item), "cluster_size": sizes[index]}) for index, item in enumerate(candidates)]

    @staticmethod
    def _tokens(title: str) -> set[str]:
        latin = set(re.findall(r"[a-z0-9]{3,}", title.casefold()))
        chinese = set(re.findall(r"[\u4e00-\u9fff]{2,4}", title))
        return latin | chinese
