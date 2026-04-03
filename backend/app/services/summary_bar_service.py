"""상단 요약 바 서비스."""
from app.cache.cache_keys import summary_bar_key, fx_key
from app.cache.cache_manager import cache_manager
from app.schemas.summary_bar import SummaryBarResponse, IndexItem, FxItem

INDEX_ORDER = ["KOSPI", "KOSDAQ", "SP500", "NASDAQ100", "DOW", "SOX", "VIX", "US10Y"]
FX_PAIRS = ["USDKRW", "JPYKRW", "EURKRW"]
COMMODITY_ORDER = ["WTI", "GOLD"]


async def get_summary_bar() -> SummaryBarResponse:
    bar_data = await cache_manager.get(summary_bar_key()) or {}

    indices = []
    for name in INDEX_ORDER + COMMODITY_ORDER:
        d = bar_data.get(name, {})
        indices.append(IndexItem(
            name=name,
            price=d.get("price"),
            change_percent=d.get("change_percent"),
        ))

    fx = []
    for pair in FX_PAIRS:
        d = await cache_manager.get(fx_key(pair)) or {}
        fx.append(FxItem(
            pair=pair,
            rate=d.get("rate"),
            change_percent=d.get("change_percent"),
        ))

    return SummaryBarResponse(indices=indices, fx=fx)
