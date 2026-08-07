from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://api.twitterapi.io"


def load_dotenv(path: Path = Path(".env")) -> None:
    """Load simple KEY=VALUE entries without overwriting existing environment values."""
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


class TwitterAPIError(RuntimeError):
    """Raised when twitterapi.io returns an HTTP or API-level error."""


class TwitterAPIClient:
    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30,
    ) -> None:
        self.api_key = api_key or os.environ.get("TWITTERAPI_IO_KEY", "")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        if not self.api_key:
            raise ValueError(
                "TWITTERAPI_IO_KEY is required; set it in the environment or a local .env file"
            )

    def get_trends(self, woeid: int = 1, count: int = 30) -> list[dict[str, Any]]:
        if woeid <= 0:
            raise ValueError("woeid must be a positive integer")
        if count < 30:
            raise ValueError("count must be at least 30")

        payload = self._get("/twitter/trends", {"woeid": woeid, "count": count})
        if payload.get("status") != "success":
            message = payload.get("msg") or payload.get("message") or "unknown API error"
            raise TwitterAPIError(f"twitterapi.io request failed: {message}")
        trends = payload.get("trends")
        if not isinstance(trends, list):
            raise TwitterAPIError("twitterapi.io response is missing the trends list")
        normalized: list[dict[str, Any]] = []
        for item in trends:
            if not isinstance(item, dict):
                continue
            trend = item.get("trend", item)
            if isinstance(trend, dict):
                normalized.append(trend)
        return normalized

    def search_tweets(
        self,
        query: str,
        *,
        query_type: str = "Top",
        cursor: str = "",
    ) -> dict[str, Any]:
        if not query.strip():
            raise ValueError("query is required")
        if query_type not in {"Top", "Latest"}:
            raise ValueError("query_type must be Top or Latest")
        payload = self._get(
            "/twitter/tweet/advanced_search",
            {"query": query, "queryType": query_type, "cursor": cursor},
        )
        tweets = payload.get("tweets")
        if not isinstance(tweets, list):
            message = payload.get("msg") or payload.get("message") or "missing tweets list"
            raise TwitterAPIError(f"twitterapi.io search failed: {message}")
        return payload

    def get_top_tweet(self, query: str) -> dict[str, Any] | None:
        payload = self.search_tweets(query, query_type="Top")
        for tweet in payload["tweets"]:
            if isinstance(tweet, dict) and tweet.get("text"):
                return tweet
        return None

    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        query = urllib.parse.urlencode(params)
        request = urllib.request.Request(
            f"{self.base_url}{path}?{query}",
            headers={"X-API-Key": self.api_key, "Accept": "application/json"},
            method="GET",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                result = json.load(response)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise TwitterAPIError(f"twitterapi.io HTTP {exc.code}: {detail[:500]}") from exc
        except urllib.error.URLError as exc:
            raise TwitterAPIError(f"twitterapi.io connection failed: {exc.reason}") from exc
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise TwitterAPIError("twitterapi.io returned invalid JSON") from exc
        if not isinstance(result, dict):
            raise TwitterAPIError("twitterapi.io returned an unexpected response")
        return result
