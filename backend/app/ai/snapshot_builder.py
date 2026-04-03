"""AI 브리프용 입력 스냅샷 빌더."""
import hashlib
import json
from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.summary_bar_service import get_summary_bar
from app.services.sector_service import get_heatmap
from app.services.event_service import get_events


@dataclass
class IndexData:
    name: str
    change_percent: float | None


@dataclass
class FxData:
    pair: str
    change_percent: float | None


@dataclass
class SectorData:
    sector_name: str
    weighted_change_percent: float | None


@dataclass
class EventData:
    event_name: str
    country: str
    importance: str
    d_day: int


@dataclass
class MarketSnapshot:
    indices: list[IndexData] = field(default_factory=list)
    fx: list[FxData] = field(default_factory=list)
    kor_sectors: list[SectorData] = field(default_factory=list)
    us_sectors: list[SectorData] = field(default_factory=list)
    upcoming_events: list[EventData] = field(default_factory=list)


async def build_snapshot(session: AsyncSession) -> MarketSnapshot:
    summary = await get_summary_bar()
    heatmap = await get_heatmap(session)
    events_resp = await get_events(session, range_type="week", country="all", category="all")

    indices = [
        IndexData(name=item.name, change_percent=item.change_percent)
        for item in summary.indices
    ]
    fx = [
        FxData(pair=item.pair, change_percent=item.change_percent)
        for item in summary.fx
    ]
    kor_sectors = [
        SectorData(
            sector_name=s.sector_name,
            weighted_change_percent=s.weighted_change_percent,
        )
        for s in heatmap.KOR
    ]
    us_sectors = [
        SectorData(
            sector_name=s.sector_name,
            weighted_change_percent=s.weighted_change_percent,
        )
        for s in heatmap.US
    ]
    upcoming_events = [
        EventData(
            event_name=e.event_name,
            country=e.country,
            importance=e.importance,
            d_day=e.d_day,
        )
        for e in events_resp.items
        if e.importance == "high" and e.d_day <= 2
    ]

    return MarketSnapshot(
        indices=indices,
        fx=fx,
        kor_sectors=kor_sectors,
        us_sectors=us_sectors,
        upcoming_events=upcoming_events,
    )


def _get_index(snapshot: MarketSnapshot, name: str) -> float | None:
    for item in snapshot.indices:
        if item.name == name:
            return item.change_percent
    return None


def _get_fx(snapshot: MarketSnapshot, pair: str) -> float | None:
    for item in snapshot.fx:
        if item.pair == pair:
            return item.change_percent
    return None


def _get_sector(sectors: list[SectorData], name: str) -> float | None:
    for s in sectors:
        if s.sector_name == name:
            return s.weighted_change_percent
    return None


def compute_snapshot_hash(snapshot: MarketSnapshot) -> str:
    """소수점 1자리 반올림 후 SHA-256 해시 (노이즈 제거)."""
    def r(v: float | None) -> float | None:
        return round(v, 1) if v is not None else None

    key_data = {
        "nasdaq100": r(_get_index(snapshot, "NASDAQ100")),
        "sp500": r(_get_index(snapshot, "SP500")),
        "kospi": r(_get_index(snapshot, "KOSPI")),
        "usdkrw": r(_get_fx(snapshot, "USDKRW")),
        "kor_semis": r(_get_sector(snapshot.kor_sectors, "Semiconductors")),
        "us_semis": r(_get_sector(snapshot.us_sectors, "Semiconductors")),
        "events": [(e.event_name, e.d_day) for e in snapshot.upcoming_events],
    }
    serialized = json.dumps(key_data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode()).hexdigest()
