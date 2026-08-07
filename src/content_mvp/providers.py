from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from typing import Any


class ContentProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, context: dict[str, Any]) -> dict[str, str]:
        """Return news_alert, information_reframe and original_commentary."""


class TemplateProvider(ContentProvider):
    """Deterministic provider for local validation; not intended as final copy."""

    def generate(self, prompt: str, context: dict[str, Any]) -> dict[str, str]:
        del prompt
        event = context["event"]
        fact = event["verified_facts"][0].rstrip("。.!！")
        source = event["source_urls"][0]
        if event["mode"] == "trend_capture":
            return self._trend_capture(event, fact, source)
        market = event["markets"][0] if event["markets"] else None
        signal = self._market_signal(market)
        link = market["url"] if market else source
        return {
            "news_alert": f"快讯｜{fact}。{signal} 关注后续进展：{link}",
            "information_reframe": (
                f"这件事可以看三个重点：\n1）{fact}；\n2）事件仍处于{event['action_window']}阶段；"
                f"\n3）{signal}\n来源：{source}"
            ),
            "original_commentary": (
                f"{event['event_title']}真正值得关注的，不只是新闻本身，而是它会不会改变下一步结果。"
                f"{signal} 接下来应观察：{event['participation_reason']}。{link}"
            ),
        }

    @staticmethod
    def _trend_capture(event: dict[str, Any], fact: str, source: str) -> dict[str, str]:
        return {
            "news_alert": f"JUST IN: {fact}.\n\nSource: {source}",
            "information_reframe": (
                f"THE CONTEXT:\n• Confirmed: {fact}.\n"
                f"• Next watchpoint: {event['participation_reason']}.\n\nSource: {source}"
            ),
            "original_commentary": (
                f"The headline is {event['event_title']}. The real question is what happens next: "
                f"{event['participation_reason']}.\n\nSource: {source}"
            ),
        }

    @staticmethod
    def _market_signal(market: dict[str, Any] | None) -> str:
        if not market:
            return "目前没有可直接对应的 Predx 市场，不做生硬产品植入。"
        probability = market.get("probability")
        change = market.get("probability_change")
        parts = [f"Predx 对应市场“{market['title']}”"]
        if probability is not None:
            parts.append(f"当前概率 {probability:g}%")
        if change is not None:
            direction = "上升" if change >= 0 else "下降"
            parts.append(f"近期{direction} {abs(change):g} 个百分点")
        return "，".join(parts) + "。"


class OpenAICompatibleProvider(ContentProvider):
    """Small OpenAI-compatible chat client using only Python stdlib."""

    def __init__(self) -> None:
        self.base_url = os.environ.get("CONTENT_LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self.api_key = os.environ.get("CONTENT_LLM_API_KEY", "")
        self.model = os.environ.get("CONTENT_LLM_MODEL", "")
        self.reasoning_effort = os.environ.get("CONTENT_LLM_REASONING_EFFORT", "none")
        if not self.api_key or not self.model:
            raise ValueError("CONTENT_LLM_API_KEY and CONTENT_LLM_MODEL are required")

    def generate(self, prompt: str, context: dict[str, Any]) -> dict[str, str]:
        payload = {
            "model": self.model,
            "reasoning_effort": self.reasoning_effort,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": json.dumps(context, ensure_ascii=False)},
            ],
        }
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                result = json.load(response)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"LLM request failed ({exc.code}): {detail[:500]}") from exc
        content = result["choices"][0]["message"]["content"]
        drafts = json.loads(content)
        required = {"news_alert", "information_reframe", "original_commentary"}
        if not required.issubset(drafts):
            raise ValueError(f"LLM response missing keys: {sorted(required - set(drafts))}")
        return {key: str(drafts[key]).strip() for key in required}
