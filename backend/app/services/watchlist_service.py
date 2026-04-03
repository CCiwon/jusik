"""관심종목 보드 서비스."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.cache.cache_keys import fx_key
from app.cache.cache_manager import cache_manager
from app.models.instrument import Instrument
from app.schemas.watchlist import WatchlistItem, WatchlistResponse, InstrumentSearchItem


async def get_watchlist(
    session: AsyncSession,
    market: str = "all",
    sort: str = "display_order",
) -> WatchlistResponse:
    query = (
        select(Instrument)
        .options(selectinload(Instrument.quote))
        .where(Instrument.is_active.is_(True), Instrument.in_watchlist.is_(True))
    )
    if market == "kor":
        query = query.where(Instrument.market_type == "KOR")
    elif market == "us":
        query = query.where(Instrument.market_type == "US")

    query = query.order_by(Instrument.display_order)
    result = await session.execute(query)
    instruments = result.scalars().all()

    usdkrw_data = await cache_manager.get(fx_key("USDKRW"))
    usdkrw = usdkrw_data["rate"] if usdkrw_data else None

    items = []
    for inst in instruments:
        q = inst.quote
        items.append(WatchlistItem(
            symbol=inst.symbol,
            company_name=inst.company_name,
            company_name_ko=inst.company_name_ko,
            market_type=inst.market_type,
            sector=inst.sector,
            price_local=q.price_local if q else None,
            currency=inst.currency,
            price_krw=q.price_krw if q else None,
            daily_change_percent=q.daily_change_percent if q else None,
            daily_change_amount_local=q.daily_change_amount_local if q else None,
            daily_change_amount_krw=q.daily_change_amount_krw if q else None,
            session_status=q.session_status if q else "closed",
            market_cap=inst.market_cap,
            volume=q.volume if q else None,
            fx_impact_percent=q.fx_impact_percent if q else None,
        ))

    if sort == "change":
        items.sort(key=lambda x: x.daily_change_percent or 0, reverse=True)
    elif sort == "krw_delta":
        items.sort(key=lambda x: abs(x.daily_change_amount_krw or 0), reverse=True)
    elif sort == "market_cap":
        items.sort(key=lambda x: x.market_cap or 0, reverse=True)

    return WatchlistResponse(items=items, usdkrw=usdkrw)


async def toggle_watchlist(
    session: AsyncSession,
    market_type: str,
    symbol: str,
) -> dict:
    result = await session.execute(
        select(Instrument).where(
            Instrument.symbol == symbol,
            Instrument.market_type == market_type.upper(),
        )
    )
    inst = result.scalar_one_or_none()
    if not inst:
        return {"error": "not_found"}

    inst.in_watchlist = not inst.in_watchlist
    await session.commit()
    return {"symbol": symbol, "in_watchlist": inst.in_watchlist}


async def search_instruments(
    session: AsyncSession,
    query: str,
    market: str = "all",
) -> list[InstrumentSearchItem]:
    stmt = select(Instrument).where(Instrument.is_active.is_(True))

    if market == "kor":
        stmt = stmt.where(Instrument.market_type == "KOR")
    elif market == "us":
        stmt = stmt.where(Instrument.market_type == "US")

    result = await session.execute(stmt.order_by(Instrument.display_order))
    instruments = result.scalars().all()

    q_lower = query.lower()
    matched = [
        i for i in instruments
        if q_lower in i.symbol.lower()
        or q_lower in i.company_name.lower()
        or (i.company_name_ko and q_lower in i.company_name_ko.lower())
    ]

    return [
        InstrumentSearchItem(
            symbol=i.symbol,
            company_name=i.company_name,
            company_name_ko=i.company_name_ko,
            market_type=i.market_type,
            sector=i.sector,
            in_watchlist=i.in_watchlist,
        )
        for i in matched[:20]
    ]
