"""룰 기반 개장 전 브리프 규칙 정의."""
from dataclasses import dataclass
from typing import Callable

from app.ai.snapshot_builder import MarketSnapshot, _get_index, _get_fx, _get_sector


@dataclass
class BriefRule:
    id: str
    priority: int
    category: str  # market | fx | sector | event
    condition: Callable[[MarketSnapshot], bool]
    template: Callable[[MarketSnapshot], str]


def _nasdaq(s: MarketSnapshot) -> float | None:
    return _get_index(s, "NASDAQ100")

def _sp500(s: MarketSnapshot) -> float | None:
    return _get_index(s, "SP500")

def _kospi(s: MarketSnapshot) -> float | None:
    return _get_index(s, "KOSPI")

def _usdkrw(s: MarketSnapshot) -> float | None:
    return _get_fx(s, "USDKRW")

def _us_semis(s: MarketSnapshot) -> float | None:
    return _get_sector(s.us_sectors, "Semiconductors")

def _kor_semis(s: MarketSnapshot) -> float | None:
    return _get_sector(s.kor_sectors, "Semiconductors")

def _us_energy(s: MarketSnapshot) -> float | None:
    return _get_sector(s.us_sectors, "Energy")

def _has_high_event_today(s: MarketSnapshot) -> bool:
    return any(e.importance == "high" and e.d_day == 0 for e in s.upcoming_events)

def _has_high_event_tomorrow(s: MarketSnapshot) -> bool:
    return any(e.importance == "high" and e.d_day == 1 for e in s.upcoming_events)

def _get_today_event_names(s: MarketSnapshot) -> str:
    names = [e.event_name for e in s.upcoming_events if e.importance == "high" and e.d_day == 0]
    return ", ".join(names[:2])

def _get_tomorrow_event_names(s: MarketSnapshot) -> str:
    names = [e.event_name for e in s.upcoming_events if e.importance == "high" and e.d_day == 1]
    return ", ".join(names[:2])


OPENING_BRIEF_RULES: list[BriefRule] = [
    # ── market ──────────────────────────────────────────────────
    BriefRule(
        id="nasdaq_strong",
        priority=10,
        category="market",
        condition=lambda s: (_nasdaq(s) or 0) >= 1.0,
        template=lambda s: f"간밤 미국 나스닥이 {_nasdaq(s):+.1f}% 강세를 보였습니다.",
    ),
    BriefRule(
        id="nasdaq_weak",
        priority=10,
        category="market",
        condition=lambda s: (_nasdaq(s) or 0) <= -1.0,
        template=lambda s: f"간밤 미국 나스닥이 {_nasdaq(s):+.1f}% 하락하며 약세로 마감했습니다.",
    ),
    BriefRule(
        id="sp500_strong",
        priority=9,
        category="market",
        condition=lambda s: (_sp500(s) or 0) >= 0.5 and abs((_nasdaq(s) or 0)) < 1.0,
        template=lambda s: f"간밤 S&P500이 {_sp500(s):+.1f}%로 상승 마감했습니다.",
    ),
    BriefRule(
        id="sp500_weak",
        priority=9,
        category="market",
        condition=lambda s: (_sp500(s) or 0) <= -0.5 and abs((_nasdaq(s) or 0)) < 1.0,
        template=lambda s: f"간밤 S&P500이 {_sp500(s):+.1f}%로 하락 마감했습니다.",
    ),
    BriefRule(
        id="market_flat",
        priority=5,
        category="market",
        condition=lambda s: abs((_nasdaq(s) or 0)) < 0.5 and abs((_sp500(s) or 0)) < 0.5,
        template=lambda s: "간밤 미국 증시는 보합권에서 마감했습니다.",
    ),
    # ── sector ──────────────────────────────────────────────────
    BriefRule(
        id="semis_both_strong",
        priority=12,
        category="sector",
        condition=lambda s: (_us_semis(s) or 0) >= 1.0 and (_kor_semis(s) is not None),
        template=lambda s: (
            f"미국 반도체 섹터가 {_us_semis(s):+.1f}% 강세를 보여 "
            "국장 반도체 대형주에 우호적인 흐름이 기대됩니다."
        ),
    ),
    BriefRule(
        id="semis_us_weak",
        priority=11,
        category="sector",
        condition=lambda s: (_us_semis(s) or 0) <= -1.0,
        template=lambda s: (
            f"미국 반도체 섹터가 {_us_semis(s):+.1f}% 하락해 "
            "국장 반도체주에 부정적인 영향이 예상됩니다."
        ),
    ),
    BriefRule(
        id="energy_strong",
        priority=8,
        category="sector",
        condition=lambda s: (_us_energy(s) or 0) >= 1.5,
        template=lambda s: (
            f"에너지 섹터가 {_us_energy(s):+.1f}% 강세를 보여 "
            "원자재·에너지 관련주에 주목이 필요합니다."
        ),
    ),
    # ── fx ──────────────────────────────────────────────────────
    BriefRule(
        id="usdkrw_strong",
        priority=10,
        category="fx",
        condition=lambda s: (_usdkrw(s) or 0) >= 0.5,
        template=lambda s: (
            f"달러-원 환율이 {_usdkrw(s):+.1f}% 상승해 외국인 수급에 "
            "보수적 시각이 필요합니다."
        ),
    ),
    BriefRule(
        id="usdkrw_weak",
        priority=10,
        category="fx",
        condition=lambda s: (_usdkrw(s) or 0) <= -0.5,
        template=lambda s: (
            f"달러-원 환율이 {_usdkrw(s):+.1f}% 하락해 외국인 자금 유입에 "
            "우호적인 환경이 형성될 수 있습니다."
        ),
    ),
    BriefRule(
        id="usdkrw_flat",
        priority=3,
        category="fx",
        condition=lambda s: abs((_usdkrw(s) or 0)) < 0.5,
        template=lambda s: "달러-원 환율은 보합권을 유지하고 있습니다.",
    ),
    # ── event ───────────────────────────────────────────────────
    BriefRule(
        id="high_event_today",
        priority=15,
        category="event",
        condition=_has_high_event_today,
        template=lambda s: (
            f"오늘 {_get_today_event_names(s)} 등 주요 이벤트가 예정되어 "
            "장중 변동성 확대에 유의하시기 바랍니다."
        ),
    ),
    BriefRule(
        id="high_event_tomorrow",
        priority=13,
        category="event",
        condition=lambda s: not _has_high_event_today(s) and _has_high_event_tomorrow(s),
        template=lambda s: (
            f"내일 {_get_tomorrow_event_names(s)} 발표가 예정되어 "
            "오늘 장에서도 경계 심리가 유지될 수 있습니다."
        ),
    ),
]
