from pydantic import BaseModel


class WatchlistItem(BaseModel):
    symbol: str
    company_name: str
    company_name_ko: str | None
    market_type: str
    sector: str | None
    price_local: float | None
    currency: str
    price_krw: float | None
    daily_change_percent: float | None
    daily_change_amount_local: float | None
    daily_change_amount_krw: float | None
    session_status: str
    market_cap: float | None
    volume: float | None
    fx_impact_percent: float | None


class WatchlistResponse(BaseModel):
    items: list[WatchlistItem]
    usdkrw: float | None


class InstrumentSearchItem(BaseModel):
    symbol: str
    company_name: str
    company_name_ko: str | None
    market_type: str
    sector: str | None
    in_watchlist: bool
