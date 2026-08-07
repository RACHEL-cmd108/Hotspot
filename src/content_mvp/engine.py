from __future__ import annotations

import json
import re
from dataclasses import asdict
from difflib import SequenceMatcher
from typing import Any

from .models import AccountProfile, ActionPackage
from .providers import ContentProvider, TemplateProvider


VARIANTS = ("news_alert", "information_reframe", "original_commentary")
WEIGHTS = {
    "market_match": 0.30,
    "outcome_impact": 0.25,
    "market_signal": 0.20,
    "audience_overlap": 0.15,
    "natural_fit": 0.10,
}
HEAT_WEIGHTS = {
    "source_reliability": 0.30,
    "freshness": 0.25,
    "velocity": 0.25,
    "audience_fit": 0.20,
}


class ContentEngine:
    def __init__(self, provider: ContentProvider | None = None) -> None:
        self.provider = provider or TemplateProvider()

    def run(self, action: ActionPackage, account: AccountProfile) -> dict[str, Any]:
        score = self._score(action)
        decision, allowed = self._gate(score, action.mode)
        result: dict[str, Any] = {
            "event_id": action.event_id,
            "account": account.handle,
            "relevance_score": score,
            "mode": action.mode,
            "decision": decision,
            "drafts": {},
            "quality": {"passed": False, "issues": []},
        }
        if not allowed:
            message = (
                "热度或账号适配不足，暂不承接"
                if action.mode == "trend_capture"
                else "产品相关性低于 40，拒绝硬蹭热点"
            )
            result["quality"]["issues"].append(message)
            return result

        context = {"event": asdict(action), "account": asdict(account), "allowed_variants": allowed}
        generated = self.provider.generate(self._prompt(), context)
        drafts = {name: generated[name] for name in allowed}
        issues = self._quality_check(drafts, action, account)
        result["drafts"] = drafts
        result["quality"] = {"passed": not issues, "issues": issues}
        return result

    @staticmethod
    def _score(action: ActionPackage) -> float:
        dimensions = action.heat if action.mode == "trend_capture" else action.relevance
        weights = HEAT_WEIGHTS if action.mode == "trend_capture" else WEIGHTS
        missing = set(weights) - set(dimensions)
        if missing:
            label = "heat" if action.mode == "trend_capture" else "relevance"
            raise ValueError(f"{label} missing dimensions: {sorted(missing)}")
        score = sum(max(0, min(100, dimensions[key])) * weight for key, weight in weights.items())
        return round(score, 1)

    @staticmethod
    def _gate(score: float, mode: str) -> tuple[str, tuple[str, ...]]:
        if score < 40:
            return "reject_low_heat" if mode == "trend_capture" else "reject", ()
        if score < 60:
            return ("watch", ()) if mode == "trend_capture" else ("weak_fit", ("news_alert",))
        if score < 80:
            return ("capture", VARIANTS) if mode == "trend_capture" else ("participate", VARIANTS)
        return "priority_capture" if mode == "trend_capture" else "strong_fit", VARIANTS

    @staticmethod
    def _quality_check(
        drafts: dict[str, str], action: ActionPackage, account: AccountProfile
    ) -> list[str]:
        issues: list[str] = []
        prohibited = action.prohibited_claims + account.prohibited_phrases
        allowed_text = json.dumps(asdict(action), ensure_ascii=False)
        allowed_numbers = set(re.findall(r"(?<![\w])[-+]?\d+(?:\.\d+)?", allowed_text))

        for name, text in drafts.items():
            if not text.strip():
                issues.append(f"{name}: 内容为空")
                continue
            if len(text) > account.max_chars:
                issues.append(f"{name}: {len(text)} 字符，超过账号上限 {account.max_chars}")
            for phrase in prohibited:
                if phrase and phrase.lower() in text.lower():
                    issues.append(f"{name}: 包含禁用表述“{phrase}”")
            draft_numbers = set(re.findall(r"(?<![\w])[-+]?\d+(?:\.\d+)?", text))
            unsupported = draft_numbers - allowed_numbers - {"1", "2", "3"}
            if unsupported:
                issues.append(f"{name}: 出现输入中不存在的数字 {sorted(unsupported)}")
            if not any(url in text for url in action.source_urls) and not any(
                market.url in text for market in action.markets
            ):
                issues.append(f"{name}: 缺少来源或市场链接")

        names = list(drafts)
        for index, left in enumerate(names):
            for right in names[index + 1 :]:
                similarity = SequenceMatcher(None, drafts[left], drafts[right]).ratio()
                if similarity >= 0.78:
                    issues.append(f"{left}/{right}: 内容相似度 {similarity:.0%}，版本区分不足")
        return issues

    @staticmethod
    def _prompt() -> str:
        return """你是 Predx 的 X 内容编辑。只可使用输入中的已确认事实、来源和市场数据。
生成严格 JSON，键为 news_alert、information_reframe、original_commentary。
news_alert：简短准确的新闻通知；information_reframe：重组多个事实并提供结构价值，不得同义词洗稿；
original_commentary：增加原创判断、情景或值得继续观察的变量，但不得创造新事实。
当 mode=trend_capture 时，不得提及 Predx 产品或市场，只承接热点本身；账号画像只用于学习结构、节奏和语气，不得复刻示例原句。
当 mode=product_relevance 时，产品关联必须来自 markets；没有自然关联时明确不植入。不得作收益承诺或金融建议。
遵守账号语言、语气、字数和禁用表达。每个版本保留至少一个来源或市场链接。"""
