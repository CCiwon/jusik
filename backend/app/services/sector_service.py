"""섹터 히트맵 집계 서비스."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.instrument import Instrument
from app.schemas.sector import SectorItem, HeatmapResponse

SECTOR_KO_MAP = {
    "Semiconductors": "반도체",
    "Battery": "2차전지",
    "Automobile": "자동차",
    "Internet": "인터넷",
    "Bio": "바이오",
    "Finance": "금융",
    "Shipbuilding": "조선",
    "Defense": "방산",
    "Energy": "에너지",
    "Chemical": "화학",
    "Big Tech": "빅테크",
    "Consumer": "소비재",
    "Healthcare": "헬스케어",
    "Industrials": "산업재",
    "Communication": "통신",
}


async def get_heatmap(session: AsyncSession) -> HeatmapResponse:
    result = await session.execute(
        select(Instrument)
        .options(selectinload(Instrument.quote))
        .where(Instrument.is_active.is_(True))
    )
    instruments = result.scalars().all()

    kor_map: dict[str, list] = {}
    us_map: dict[str, list] = {}

    for inst in instruments:
        if not inst.sector:
            continue
        target = kor_map if inst.market_type == "KOR" else us_map
        target.setdefault(inst.sector, []).append(inst)

    def build_sectors(sector_map: dict) -> list[SectorItem]:
        sectors = []
        for sector_name, insts in sector_map.items():
            total_cap = sum(i.market_cap or 0 for i in insts)
            weighted_change = None

            if total_cap > 0:
                weighted_change = sum(
                    (i.quote.daily_change_percent or 0) * (i.market_cap or 0)
                    for i in insts
                    if i.quote
                ) / total_cap

            sorted_by_change = sorted(
                [i for i in insts if i.quote and i.quote.daily_change_percent is not None],
                key=lambda x: x.quote.daily_change_percent,
            )
            strongest = sorted_by_change[-1].symbol if sorted_by_change else None
            weakest = sorted_by_change[0].symbol if sorted_by_change else None

            instrument_list = [
                {
                    "symbol": i.symbol,
                    "name": i.company_name_ko or i.company_name,
                    "change_percent": i.quote.daily_change_percent if i.quote else None,
                    "market_cap": i.market_cap,
                }
                for i in insts
            ]

            sectors.append(SectorItem(
                sector_name=sector_name,
                sector_name_ko=SECTOR_KO_MAP.get(sector_name),
                weighted_change_percent=round(weighted_change, 4) if weighted_change else None,
                total_market_cap=total_cap,
                strongest_symbol=strongest,
                weakest_symbol=weakest,
                instruments=instrument_list,
            ))

        return sorted(sectors, key=lambda s: s.weighted_change_percent or 0, reverse=True)

    kor_sectors = build_sectors(kor_map)
    us_sectors = build_sectors(us_map)

    all_sectors = kor_sectors + us_sectors
    top = [s.sector_name for s in sorted(all_sectors, key=lambda s: s.weighted_change_percent or 0, reverse=True)[:3]]
    bottom = [s.sector_name for s in sorted(all_sectors, key=lambda s: s.weighted_change_percent or 0)[:3]]

    return HeatmapResponse(KOR=kor_sectors, US=us_sectors, top_sectors=top, bottom_sectors=bottom)
