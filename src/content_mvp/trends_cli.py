from __future__ import annotations

import argparse
import json
from pathlib import Path

from .twitterapi import TwitterAPIClient, load_dotenv


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch X trends from twitterapi.io")
    parser.add_argument("--woeid", type=int, default=1, help="Location WOEID (default: 1, worldwide)")
    parser.add_argument("--count", type=int, default=30, help="Number of trends (minimum: 30)")
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    load_dotenv(args.env_file)
    trends = TwitterAPIClient().get_trends(woeid=args.woeid, count=args.count)
    rendered = json.dumps(
        {"source": "twitterapi.io", "woeid": args.woeid, "count": len(trends), "trends": trends},
        ensure_ascii=False,
        indent=2,
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(args.output)
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
