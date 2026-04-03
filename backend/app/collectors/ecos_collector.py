"""한국은행 ECOS API 환율 수집기."""
import logging
from dataclasses import dataclass
from datetime import date, timedelta

from app.collectors.base_collector import BaseCollector
from app.config import settings

logger = logging.getLogger(__name__)

ECOS_BASE = "https://ecos.bok.or.kr/api/StatisticSearch"

# 매매기준율 통계표 코드 및 항목코드
FX_PAIRS = [
    {"pair": "USDKRW", "item_code": "0000001", "base": "USD", "target": "KRW"},
    {"pair": "JPYKRW", "item_code": "0000002", "base": "JPY", "target": "KRW"},
    {"pair": "EURKRW", "item_code": "0000003", "base": "EUR", "target": "KRW"},
]
STAT_CODE = "731Y001"


@dataclass
class FxRateData:
    pair: str
    base_currency: str
    target_currency: str
    rate: float
    prev_rate: float | None
    change_percent: float | None


class EcosCollector(BaseCollector):
    async def collect(self) -> list[FxRateData]:
        results = []
        today = date.today()
        yesterday = today - timedelta(days=3)  # 주말 대비 3일 여유

        for fx in FX_PAIRS:
            try:
                data = await self._fetch_fx(fx, yesterday, today)
                if data:
                    results.append(data)
            except Exception as e:
                logger.error(f"ECOS fetch failed for {fx['pair']}: {e}")

        return results

    async def _fetch_fx(self, fx: dict, start: date, end: date) -> FxRateData | None:
        url = (
            f"{ECOS_BASE}/{settings.ecos_api_key}/json/kr/1/10"
            f"/{STAT_CODE}/D"
            f"/{start.strftime('%Y%m%d')}/{end.strftime('%Y%m%d')}"
            f"/{fx['item_code']}"
        )
        data = await self.get(url)

        rows = data.get("StatisticSearch", {}).get("row", [])
        if not rows:
            logger.warning(f"ECOS: no data for {fx['pair']}")
            return None

        # 최신 데이터가 마지막
        rows_sorted = sorted(rows, key=lambda r: r.get("TIME", ""))
        latest = rows_sorted[-1]
        prev = rows_sorted[-2] if len(rows_sorted) >= 2 else None

        rate = float(latest["DATA_VALUE"])
        prev_rate = float(prev["DATA_VALUE"]) if prev else None
        change_pct = ((rate - prev_rate) / prev_rate * 100) if prev_rate else None

        return FxRateData(
            pair=fx["pair"],
            base_currency=fx["base"],
            target_currency=fx["target"],
            rate=rate,
            prev_rate=prev_rate,
            change_percent=round(change_pct, 4) if change_pct else None,
        )
