"""yfinance 기반 한국 주식 및 지수 수집기."""
import asyncio
import logging
from dataclasses import dataclass
from functools import partial

import yfinance as yf

logger = logging.getLogger(__name__)

# 한국 지수 심볼
KOR_INDICES = {
    "KOSPI": "^KS11",
    "KOSDAQ": "^KQ11",
}

# yfinance로 수집하는 글로벌 지수
GLOBAL_INDICES = {
    "US10Y": "^TNX",  # 미국 10년 국채 금리
    "VIX": "^VIX",    # 시장 공포 지수
}

# KOSPI 심볼은 .KS, KOSDAQ은 .KQ
KOSDAQ_SYMBOLS = {"247540", "259960", "042700", "058470"}


@dataclass
class QuoteData:
    symbol: str
    market_type: str
    price: float | None
    prev_close: float | None
    change_percent: float | None
    change_amount: float | None
    session_status: str
    volume: float | None = None


@dataclass
class IndexData:
    name: str
    price: float | None
    prev_close: float | None
    change_percent: float | None


class YfinanceCollector:
    """yfinance는 async 미지원이라 스레드풀에서 실행."""

    def _get_suffix(self, symbol: str) -> str:
        return ".KQ" if symbol in KOSDAQ_SYMBOLS else ".KS"

    def _fetch_quote_sync(self, symbol: str) -> QuoteData:
        suffix = self._get_suffix(symbol)
        ticker = yf.Ticker(f"{symbol}{suffix}")
        try:
            info = ticker.fast_info
            price = getattr(info, "last_price", None)
            prev_close = getattr(info, "previous_close", None)

            if price and prev_close:
                change_amount = price - prev_close
                change_pct = (change_amount / prev_close) * 100
            else:
                change_amount = None
                change_pct = None

            volume = getattr(info, "three_month_average_volume", None)
            return QuoteData(
                symbol=symbol,
                market_type="KOR",
                price=round(price, 2) if price else None,
                prev_close=round(prev_close, 2) if prev_close else None,
                change_percent=round(change_pct, 4) if change_pct else None,
                change_amount=round(change_amount, 2) if change_amount else None,
                session_status="open",
                volume=float(volume) if volume else None,
            )
        except Exception as e:
            logger.warning(f"yfinance fetch failed for {symbol}: {e}")
            return QuoteData(
                symbol=symbol, market_type="KOR",
                price=None, prev_close=None,
                change_percent=None, change_amount=None,
                session_status="closed",
            )

    def _fetch_index_sync(self, name: str, yf_symbol: str) -> IndexData:
        ticker = yf.Ticker(yf_symbol)
        try:
            info = ticker.fast_info
            price = getattr(info, "last_price", None)
            prev_close = getattr(info, "previous_close", None)
            change_pct = (
                ((price - prev_close) / prev_close * 100)
                if price and prev_close else None
            )
            return IndexData(
                name=name,
                price=round(price, 2) if price else None,
                prev_close=round(prev_close, 2) if prev_close else None,
                change_percent=round(change_pct, 4) if change_pct else None,
            )
        except Exception as e:
            logger.warning(f"yfinance index fetch failed for {name}: {e}")
            return IndexData(name=name, price=None, prev_close=None, change_percent=None)

    async def collect_quotes(self, symbols: list[str]) -> list[QuoteData]:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(None, partial(self._fetch_quote_sync, sym))
            for sym in symbols
        ]
        return list(await asyncio.gather(*tasks))

    def _fetch_us_volume_sync(self, symbol: str) -> tuple[str, float | None]:
        ticker = yf.Ticker(symbol)
        try:
            volume = getattr(ticker.fast_info, "three_month_average_volume", None)
            return symbol, float(volume) if volume else None
        except Exception:
            return symbol, None

    async def collect_us_volumes(self, symbols: list[str]) -> dict[str, float | None]:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(None, partial(self._fetch_us_volume_sync, sym))
            for sym in symbols
        ]
        results = await asyncio.gather(*tasks)
        return dict(results)

    async def collect_indices(self) -> list[IndexData]:
        loop = asyncio.get_event_loop()
        all_indices = {**KOR_INDICES, **GLOBAL_INDICES}
        tasks = [
            loop.run_in_executor(None, partial(self._fetch_index_sync, name, sym))
            for name, sym in all_indices.items()
        ]
        return list(await asyncio.gather(*tasks))
