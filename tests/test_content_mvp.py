import unittest
import sqlite3
import tempfile
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from content_mvp.engine import ContentEngine
from content_mvp.models import AccountProfile, ActionPackage
from content_mvp.trendradar import TrendRadarAdapter
from content_mvp.twitterapi import TwitterAPIClient, TwitterAPIError


def action(score: float = 80) -> ActionPackage:
    return ActionPackage.from_dict(
        {
            "event_id": "e1",
            "event_title": "测试事件",
            "verified_facts": ["官方确认测试事件发生"],
            "source_urls": ["https://example.com/source"],
            "action_window": "breaking",
            "objective": "awareness",
            "audience": ["测试用户"],
            "participation_reason": "观察下一步影响",
            "risks": [],
            "prohibited_claims": ["稳赚"],
            "markets": [
                {
                    "market_id": "m1",
                    "title": "测试市场",
                    "probability": 60,
                    "probability_change": 5,
                    "url": "https://example.com/market",
                }
            ],
            "relevance": {key: score for key in (
                "market_match", "outcome_impact", "market_signal", "audience_overlap", "natural_fit"
            )},
        }
    )


def account() -> AccountProfile:
    return AccountProfile.from_dict(
        {
            "handle": "@test",
            "positioning": "测试账号",
            "audience": ["测试用户"],
            "tone": ["准确"],
            "max_chars": 280,
        }
    )


class ContentEngineTests(unittest.TestCase):
    def test_strong_fit_generates_three_variants(self):
        result = ContentEngine().run(action(85), account())
        self.assertEqual(result["decision"], "strong_fit")
        self.assertEqual(len(result["drafts"]), 3)

    def test_weak_fit_only_generates_news(self):
        result = ContentEngine().run(action(50), account())
        self.assertEqual(result["decision"], "weak_fit")
        self.assertEqual(set(result["drafts"]), {"news_alert"})

    def test_low_fit_is_rejected(self):
        result = ContentEngine().run(action(30), account())
        self.assertEqual(result["decision"], "reject")
        self.assertFalse(result["drafts"])

    def test_trend_capture_does_not_require_market(self):
        data = {
            "event_id": "heat1",
            "event_title": "Breaking test",
            "verified_facts": ["An official source confirmed the test event"],
            "source_urls": ["https://example.com/source"],
            "action_window": "breaking",
            "objective": "hotspot_capture",
            "audience": ["news users"],
            "participation_reason": "Watch for the next official update",
            "mode": "trend_capture",
            "heat": {
                "source_reliability": 90,
                "freshness": 90,
                "velocity": 80,
                "audience_fit": 80
            }
        }
        result = ContentEngine().run(ActionPackage.from_dict(data), account())
        self.assertEqual(result["decision"], "priority_capture")
        self.assertEqual(len(result["drafts"]), 3)
        self.assertNotIn("Predx", " ".join(result["drafts"].values()))


class TrendRadarAdapterTests(unittest.TestCase):
    def test_reads_latest_database_and_builds_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            news = root / "output" / "news"
            news.mkdir(parents=True)
            database = news / "2026-08-04.db"
            connection = sqlite3.connect(database)
            connection.executescript(
                """
                CREATE TABLE platforms (id TEXT PRIMARY KEY, name TEXT, is_active INTEGER);
                CREATE TABLE news_items (
                    id INTEGER PRIMARY KEY, title TEXT, platform_id TEXT, rank INTEGER,
                    url TEXT, first_crawl_time TEXT, last_crawl_time TEXT, crawl_count INTEGER
                );
                CREATE TABLE rank_history (
                    id INTEGER PRIMARY KEY, news_item_id INTEGER, rank INTEGER, crawl_time TEXT
                );
                INSERT INTO platforms VALUES ('cls-hot', '财联社热门', 1);
                INSERT INTO news_items VALUES (
                    1, 'Bitcoin market test headline', 'cls-hot', 2,
                    'https://example.com/story', '10-00', '10-30', 2
                );
                INSERT INTO rank_history VALUES (1, 1, 5, '10-00');
                INSERT INTO rank_history VALUES (2, 1, 2, '10-30');
                """
            )
            connection.commit()
            connection.close()

            adapter = TrendRadarAdapter(root)
            found_db, candidates = adapter.read_candidates()
            package = adapter.to_action_package(candidates[0], account(), found_db)
            self.assertEqual(found_db, database)
            self.assertEqual(candidates[0].previous_rank, 5)
            self.assertEqual(package.mode, "trend_capture")
            self.assertEqual(package.source_urls, ["https://example.com/story"])


class TwitterAPIClientTests(unittest.TestCase):
    @patch("content_mvp.twitterapi.urllib.request.urlopen")
    def test_get_trends(self, urlopen):
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = json.dumps(
            {
                "status": "success",
                "trends": [
                    {"trend": {"name": "AI", "rank": 1, "target": {"query": "AI"}}}
                ],
            }
        ).encode("utf-8")
        urlopen.return_value = response

        trends = TwitterAPIClient("test-key").get_trends(woeid=1, count=30)

        self.assertEqual(trends[0]["name"], "AI")
        request = urlopen.call_args.args[0]
        self.assertIn("woeid=1", request.full_url)
        self.assertIn("count=30", request.full_url)
        self.assertEqual(request.headers["X-api-key"], "test-key")

    def test_rejects_count_below_api_minimum(self):
        with self.assertRaises(ValueError):
            TwitterAPIClient("test-key").get_trends(count=29)

    @patch.object(TwitterAPIClient, "_get")
    def test_raises_api_error(self, get):
        get.return_value = {"status": "error", "msg": "invalid woeid"}
        with self.assertRaises(TwitterAPIError):
            TwitterAPIClient("test-key").get_trends()

    @patch.object(TwitterAPIClient, "search_tweets")
    def test_get_top_tweet(self, search):
        search.return_value = {
            "tweets": [
                {"id": "1", "text": "Representative tweet"},
                {"id": "2", "text": "Second tweet"},
            ]
        }
        tweet = TwitterAPIClient("test-key").get_top_tweet("AI")
        self.assertEqual(tweet["id"], "1")
        search.assert_called_once_with("AI", query_type="Top")


if __name__ == "__main__":
    unittest.main()
