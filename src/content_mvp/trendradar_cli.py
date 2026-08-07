from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .engine import ContentEngine
from .models import AccountProfile
from .providers import OpenAICompatibleProvider, TemplateProvider
from .trendradar import TrendRadarAdapter


def main() -> int:
    parser = argparse.ArgumentParser(description="TrendRadar to X draft pipeline")
    parser.add_argument("--trendradar-root", type=Path, default=Path("TrendRadar"))
    parser.add_argument("--account", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/content_mvp/trendradar_drafts.json"))
    parser.add_argument("--scan-limit", type=int, default=100)
    parser.add_argument("--draft-limit", type=int, default=10)
    parser.add_argument("--min-score", type=float, default=60.0)
    parser.add_argument("--provider", choices=("template", "llm"), default="template")
    args = parser.parse_args()

    account = AccountProfile.from_dict(json.loads(args.account.read_text(encoding="utf-8")))
    adapter = TrendRadarAdapter(args.trendradar_root)
    database, candidates = adapter.read_candidates(args.scan_limit)
    provider = OpenAICompatibleProvider() if args.provider == "llm" else TemplateProvider()
    engine = ContentEngine(provider)

    ranked = []
    for candidate in candidates:
        action = adapter.to_action_package(candidate, account, database)
        result = engine.run(action, account)
        ranked.append((result["relevance_score"], candidate, action, result))
    ranked.sort(key=lambda item: item[0], reverse=True)
    selected = [item for item in ranked if item[0] >= args.min_score][: args.draft_limit]

    report = {
        "pipeline": "trendradar_to_x_drafts",
        "source_database": str(database.resolve()),
        "account": account.handle,
        "scanned": len(candidates),
        "selected": len(selected),
        "score_note": "velocity uses rank/movement/persistence; when only one crawl exists it falls back to current rank and cross-platform clustering",
        "items": [
            {
                "candidate": adapter.candidate_metadata(candidate),
                "action_package": asdict(action),
                "generation": result,
            }
            for _, candidate, action, result in selected
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"source: {database}")
    print(f"scanned: {len(candidates)}; selected: {len(selected)}")
    print(f"output: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
