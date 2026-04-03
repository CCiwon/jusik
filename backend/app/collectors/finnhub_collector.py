"""Finnhub API 수집기 — 미국 주식, 지수, 원자재, 경제 일정."""
import logging
from dataclasses import dataclass
from datetime import date, timedelta, datetime, timezone

from app.collectors.base_collector import BaseCollector
from app.config import settings

logger = logging.getLogger(__name__)

FINNHUB_BASE = "https://finnhub.io/api/v1"

# 지수/원자재는 ETF 심볼로 대체
INDEX_SYMBOLS = {
    "SP500": "SPY",
    "NASDAQ100": "QQQ",
    "DOW": "DIA",
    "SOX": "SOXX",
}
COMMODITY_SYMBOLS = {
    "WTI": "USO",
    "GOLD": "GLD",
}


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
    symbol: str
    price: float | None
    prev_close: float | None
    change_percent: float | None


@dataclass
class EconomicEventData:
    country: str
    event_name: str
    event_time: datetime
    importance: str
    previous_value: str | None
    forecast_value: str | None
    actual_value: str | None


class FinnhubCollector(BaseCollector):
    def _headers(self) -> dict:
        return {"X-Finnhub-Token": settings.finnhub_api_key}

    async def collect(self) -> list[QuoteData]:
        return []

    async def collect_quote(self, symbol: str) -> QuoteData:
        try:
            data = await self.get(
                f"{FINNHUB_BASE}/quote",
                params={"symbol": symbol},
                headers=self._headers(),
            )
            price = data.get("c") or None
            prev_close = data.get("pc") or None
            change_pct = data.get("dp") or None
            change_amt = data.get("d") or None

            return QuoteData(
                symbol=symbol,
                market_type="US",
                price=price,
                prev_close=prev_close,
                change_percent=round(change_pct, 4) if change_pct else None,
                change_amount=round(change_amt, 4) if change_amt else None,
                session_status="open",
            )
        except Exception as e:
            logger.error(f"Finnhub quote failed for {symbol}: {e}")
            return QuoteData(
                symbol=symbol, market_type="US",
                price=None, prev_close=None,
                change_percent=None, change_amount=None,
                session_status="closed",
            )

    async def collect_quotes(self, symbols: list[str]) -> list[QuoteData]:
        results = []
        for symbol in symbols:
            quote = await self.collect_quote(symbol)
            results.append(quote)
        return results

    async def collect_indices(self) -> list[IndexData]:
        results = []
        all_symbols = {**INDEX_SYMBOLS, **COMMODITY_SYMBOLS}
        for name, symbol in all_symbols.items():
            try:
                data = await self.get(
                    f"{FINNHUB_BASE}/quote",
                    params={"symbol": symbol},
                    headers=self._headers(),
                )
                results.append(IndexData(
                    name=name,
                    symbol=symbol,
                    price=data.get("c"),
                    prev_close=data.get("pc"),
                    change_percent=data.get("dp"),
                ))
            except Exception as e:
                logger.error(f"Finnhub index failed for {name}: {e}")
        return results

    async def collect_economic_events(
        self, days_ahead: int = 7
    ) -> list[EconomicEventData]:
        today = date.today()
        end = today + timedelta(days=days_ahead)
        try:
            data = await self.get(
                f"{FINNHUB_BASE}/calendar/economic",
                params={"from": today.isoformat(), "to": end.isoformat()},
                headers=self._headers(),
            )
            events = []
            for item in data.get("economicCalendar", []):
                try:
                    event_time = datetime.fromisoformat(
                        item.get("time", "").replace("Z", "+00:00")
                    )
                except (ValueError, AttributeError):
                    event_time = datetime.now(timezone.utc)

                impact = item.get("impact", "").lower()
                importance = (
                    "high" if impact == "high"
                    else "low" if impact == "low"
                    else "medium"
                )

                events.append(EconomicEventData(
                    country="US",
                    event_name=item.get("event", ""),
                    event_time=event_time,
                    importance=importance,
                    previous_value=str(item["prev"]) if item.get("prev") is not None else None,
                    forecast_value=str(item["estimate"]) if item.get("estimate") is not None else None,
                    actual_value=str(item["actual"]) if item.get("actual") is not None else None,
                ))
            return events
        except Exception as e:
            logger.error(f"Finnhub economic calendar failed: {e}")
            return []

    async def collect_earnings_events(
        self, days_ahead: int = 7
    ) -> list[EconomicEventData]:
        today = date.today()
        end = today + timedelta(days=days_ahead)
        try:
            data = await self.get(
                f"{FINNHUB_BASE}/calendar/earnings",
                params={"from": today.isoformat(), "to": end.isoformat()},
                headers=self._headers(),
            )
            events = []
            for item in data.get("earningsCalendar", []):
                try:
                    event_time = datetime.fromisoformat(
                        f"{item.get('date', today.isoformat())}T21:00:00+00:00"
                    )
                except (ValueError, AttributeError):
                    event_time = datetime.now(timezone.utc)

                events.append(EconomicEventData(
                    country="US",
                    event_name=f"{item.get('symbol', '')} 실적 발표",
                    event_time=event_time,
                    importance="high",
                    previous_value=str(item["epsActual"]) if item.get("epsActual") is not None else None,
                    forecast_value=str(item["epsEstimate"]) if item.get("epsEstimate") is not None else None,
                    actual_value=None,
                ))
            return events
        except Exception as e:
            logger.error(f"Finnhub earnings calendar failed: {e}")
            return []
