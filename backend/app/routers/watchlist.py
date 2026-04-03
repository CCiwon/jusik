from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.watchlist import WatchlistResponse, InstrumentSearchItem
from app.services.watchlist_service import get_watchlist, toggle_watchlist, search_instruments

router = APIRouter(prefix="/api", tags=["watchlist"])


@router.get("/watchlist", response_model=WatchlistResponse)
async def watchlist(
    market: Literal["all", "kor", "us"] = "all",
    sort: Literal["display_order", "change", "krw_delta", "market_cap"] = "display_order",
    session: AsyncSession = Depends(get_db),
):
    return await get_watchlist(session, market=market, sort=sort)


@router.patch("/watchlist/{market_type}/{symbol}")
async def toggle(
    market_type: str,
    symbol: str,
    session: AsyncSession = Depends(get_db),
):
    result = await toggle_watchlist(session, market_type, symbol)
    if "error" in result:
        raise HTTPException(status_code=404, detail="Instrument not found")
    return result


@router.get("/instruments/search", response_model=list[InstrumentSearchItem])
async def instrument_search(
    q: str = "",
    market: Literal["all", "kor", "us"] = "all",
    session: AsyncSession = Depends(get_db),
):
    return await search_instruments(session, query=q, market=market)
