from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import ContentEngine
from .models import AccountProfile, ActionPackage
from .providers import OpenAICompatibleProvider, TemplateProvider


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate three Predx X content variants")
    parser.add_argument("--action", required=True, type=Path)
    parser.add_argument("--account", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--provider", choices=("template", "llm"), default="template")
    args = parser.parse_args()

    action = ActionPackage.from_dict(json.loads(args.action.read_text(encoding="utf-8")))
    account = AccountProfile.from_dict(json.loads(args.account.read_text(encoding="utf-8")))
    provider = OpenAICompatibleProvider() if args.provider == "llm" else TemplateProvider()
    result = ContentEngine(provider).run(action, account)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(args.output)
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
