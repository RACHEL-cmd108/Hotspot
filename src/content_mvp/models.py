from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def _required(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"missing required field: {key}")
    return value


@dataclass(frozen=True)
class MarketSnapshot:
    market_id: str
    title: str
    url: str
    probability: float | None = None
    probability_change: float | None = None
    volume: float | None = None
    closes_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MarketSnapshot":
        return cls(
            market_id=str(_required(data, "market_id")),
            title=str(_required(data, "title")),
            url=str(_required(data, "url")),
            probability=data.get("probability"),
            probability_change=data.get("probability_change"),
            volume=data.get("volume"),
            closes_at=data.get("closes_at"),
            updated_at=data.get("updated_at"),
        )


@dataclass(frozen=True)
class AccountProfile:
    handle: str
    positioning: str
    audience: list[str]
    tone: list[str]
    language: str = "zh-CN"
    max_chars: int = 280
    product_mention: str = "natural"
    prohibited_phrases: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    hooks: list[str] = field(default_factory=list)
    style_rules: list[str] = field(default_factory=list)
    interest_keywords: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AccountProfile":
        return cls(
            handle=str(_required(data, "handle")),
            positioning=str(_required(data, "positioning")),
            audience=list(_required(data, "audience")),
            tone=list(_required(data, "tone")),
            language=str(data.get("language", "zh-CN")),
            max_chars=int(data.get("max_chars", 280)),
            product_mention=str(data.get("product_mention", "natural")),
            prohibited_phrases=list(data.get("prohibited_phrases", [])),
            examples=list(data.get("examples", [])),
            hooks=list(data.get("hooks", [])),
            style_rules=list(data.get("style_rules", [])),
            interest_keywords=list(data.get("interest_keywords", [])),
        )


@dataclass(frozen=True)
class ActionPackage:
    event_id: str
    event_title: str
    verified_facts: list[str]
    source_urls: list[str]
    action_window: str
    objective: str
    audience: list[str]
    participation_reason: str
    risks: list[str]
    prohibited_claims: list[str]
    markets: list[MarketSnapshot]
    relevance: dict[str, float]
    mode: str = "product_relevance"
    heat: dict[str, float] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ActionPackage":
        return cls(
            event_id=str(_required(data, "event_id")),
            event_title=str(_required(data, "event_title")),
            verified_facts=list(_required(data, "verified_facts")),
            source_urls=list(_required(data, "source_urls")),
            action_window=str(_required(data, "action_window")),
            objective=str(_required(data, "objective")),
            audience=list(_required(data, "audience")),
            participation_reason=str(_required(data, "participation_reason")),
            risks=list(data.get("risks", [])),
            prohibited_claims=list(data.get("prohibited_claims", [])),
            markets=[MarketSnapshot.from_dict(item) for item in data.get("markets", [])],
            relevance={key: float(value) for key, value in data.get("relevance", {}).items()},
            mode=str(data.get("mode", "product_relevance")),
            heat={key: float(value) for key, value in data.get("heat", {}).items()},
        )
