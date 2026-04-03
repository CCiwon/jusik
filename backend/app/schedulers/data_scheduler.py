"""APScheduler 기반 데이터 수집 스케줄러."""
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from app.cache.cache_keys import (
    fx_key, quote_key, summary_bar_key, sectors_key, events_key,
    TTL_FX, TTL_EVENTS, TTL_SECTORS,
)
from app.cache.cache_manager import cache_manager
from app.collectors.ecos_collector import EcosCollector
from app.collectors.finnhub_collector import FinnhubCollector
from app.collectors.yfinance_collector import YfinanceCollector
from app.database import AsyncSessionLocal
from app.models.fx_rate import FxRate
from app.models.instrument import Instrument
from app.models.market_quote import MarketQuote
from app.models.market_event import MarketEvent
from app.utils.market_hours import get_quote_ttl, get_fx_ttl, get_session_status

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone="Asia/Seoul")


async def collect_fx() -> None:
    """환율 수집 → Redis + DB."""
    try:
        async with EcosCollector() as collector:
            rates = await collector.collect()

        async with AsyncSessionLocal() as session:
            for r in rates:
                result = await session.execute(
                    select(FxRate).where(FxRate.pair == r.pair)
                )
                existing = result.scalar_one_or_none()
                if existing:
                    existing.rate = r.rate
                    existing.prev_rate = r.prev_rate
                    existing.change_percent = r.change_percent
                else:
                    session.add(FxRate(
                        pair=r.pair,
                        base_currency=r.base_currency,
                        target_currency=r.target_currency,
                        rate=r.rate,
                        prev_rate=r.prev_rate,
                        change_percent=r.change_percent,
                    ))
            await session.commit()

        ttl = get_fx_ttl()
        for r in rates:
            await cache_manager.set(
                fx_key(r.pair),
                {"pair": r.pair, "rate": r.rate, "prev_rate": r.prev_rate, "change_percent": r.change_percent},
                ttl=ttl,
            )
        logger.info(f"FX updated: {[r.pair for r in rates]}")
    except Exception as e:
        logger.error(f"collect_fx failed: {e}")


async def collect_kor_quotes() -> None:
    """한국 주식 시세 수집 → Redis + DB."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Instrument).where(
                    Instrument.market_type == "KOR",
                    Instrument.is_active.is_(True),
                )
            )
            instruments = result.scalars().all()

        if not instruments:
            return

        symbols = [i.symbol for i in instruments]
        collector = YfinanceCollector()
        quotes = await collector.collect_quotes(symbols)

        quote_map = {q.symbol: q for q in quotes}
        ttl = get_quote_ttl("KOR")
        session_status = get_session_status("KOR")

        async with AsyncSessionLocal() as session:
            for inst in instruments:
                q = quote_map.get(inst.symbol)
                if not q or q.price is None:
                    continue

                result = await session.execute(
                    select(MarketQuote).where(MarketQuote.instrument_id == inst.id)
                )
                existing = result.scalar_one_or_none()
                if existing:
                    existing.price_local = q.price
                    existing.prev_close = q.prev_close
                    existing.daily_change_percent = q.change_percent
                    existing.daily_change_amount_local = q.change_amount
                    existing.session_status = session_status
                    existing.volume = q.volume
                else:
                    session.add(MarketQuote(
                        instrument_id=inst.id,
                        price_local=q.price,
                        price_krw=q.price,
                        prev_close=q.prev_close,
                        daily_change_percent=q.change_percent,
                        daily_change_amount_local=q.change_amount,
                        daily_change_amount_krw=q.change_amount,
                        session_status=session_status,
                        volume=q.volume,
                    ))

                await cache_manager.set(
                    quote_key("kor", inst.symbol),
                    {
                        "symbol": inst.symbol,
                        "price": q.price,
                        "change_percent": q.change_percent,
                        "session_status": session_status,
                    },
                    ttl=ttl,
                )
            await session.commit()

        logger.info(f"KOR quotes updated: {len(quotes)} symbols")
    except Exception as e:
        logger.error(f"collect_kor_quotes failed: {e}")


async def collect_us_quotes() -> None:
    """미국 주식 시세 수집 → Redis + DB."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Instrument).where(
                    Instrument.market_type == "US",
                    Instrument.is_active.is_(True),
                )
            )
            instruments = result.scalars().all()

        if not instruments:
            return

        # 환율 조회 (원화 환산용)
        usdkrw_data = await cache_manager.get(fx_key("USDKRW"))
        if not usdkrw_data:
            async with AsyncSessionLocal() as fx_session:
                fx_row = await fx_session.execute(select(FxRate).where(FxRate.pair == "USDKRW"))
                fx = fx_row.scalar_one_or_none()
                usdkrw = fx.rate if fx else None
        else:
            usdkrw = usdkrw_data["rate"]

        if not usdkrw:
            logger.warning("USDKRW rate unavailable, skipping US quote collection")
            return

        prev_usdkrw = usdkrw_data.get("prev_rate") if usdkrw_data else None

        symbols = [i.symbol for i in instruments]
        ttl = get_quote_ttl("US")
        session_status = get_session_status("US")

        async with FinnhubCollector() as collector:
            quotes = await collector.collect_quotes(symbols)

        yf_collector = YfinanceCollector()
        volume_map = await yf_collector.collect_us_volumes(symbols)

        quote_map = {q.symbol: q for q in quotes}
        for q in quotes:
            q.volume = volume_map.get(q.symbol)

        async with AsyncSessionLocal() as session:
            for inst in instruments:
                q = quote_map.get(inst.symbol)
                if not q or q.price is None:
                    continue

                price_krw = round(q.price * usdkrw, 0) if q.price else None
                change_amt_krw = (
                    round(q.change_amount * usdkrw, 0) if q.change_amount else None
                )

                # 환율 기여도: prev_usdkrw 기반으로 정확하게 계산
                fx_impact = None
                if (
                    q.change_percent is not None
                    and q.prev_close is not None
                    and prev_usdkrw
                    and price_krw
                ):
                    prev_price_krw = q.prev_close * prev_usdkrw
                    if prev_price_krw:
                        krw_change_pct = ((price_krw - prev_price_krw) / prev_price_krw) * 100
                        fx_impact = round(krw_change_pct - q.change_percent, 4)

                result = await session.execute(
                    select(MarketQuote).where(MarketQuote.instrument_id == inst.id)
                )
                existing = result.scalar_one_or_none()
                if existing:
                    existing.price_local = q.price
                    existing.price_krw = price_krw
                    existing.prev_close = q.prev_close
                    existing.daily_change_percent = q.change_percent
                    existing.daily_change_amount_local = q.change_amount
                    existing.daily_change_amount_krw = change_amt_krw
                    existing.fx_impact_percent = fx_impact
                    existing.session_status = session_status
                    existing.volume = q.volume
                else:
                    session.add(MarketQuote(
                        instrument_id=inst.id,
                        price_local=q.price,
                        price_krw=price_krw,
                        prev_close=q.prev_close,
                        daily_change_percent=q.change_percent,
                        daily_change_amount_local=q.change_amount,
                        daily_change_amount_krw=change_amt_krw,
                        fx_impact_percent=fx_impact,
                        session_status=session_status,
                        volume=q.volume,
                    ))

                await cache_manager.set(
                    quote_key("us", inst.symbol),
                    {
                        "symbol": inst.symbol,
                        "price_usd": q.price,
                        "price_krw": price_krw,
                        "change_percent": q.change_percent,
                        "session_status": session_status,
                    },
                    ttl=ttl,
                )
            await session.commit()

        logger.info(f"US quotes updated: {len(quotes)} symbols")
    except Exception as e:
        logger.error(f"collect_us_quotes failed: {e}")


async def collect_events() -> None:
    """Finnhub 경제/실적 일정 수집 → Redis + DB."""
    try:
        async with FinnhubCollector() as collector:
            eco_events = await collector.collect_economic_events(days_ahead=7)
            earn_events = await collector.collect_earnings_events(days_ahead=7)

        all_events = eco_events + earn_events

        async with AsyncSessionLocal() as session:
            from datetime import timedelta
            from app.utils.timezone import now_utc
            cutoff = now_utc() - timedelta(hours=1)
            await session.execute(
                MarketEvent.__table__.delete().where(
                    MarketEvent.event_time >= cutoff,
                    MarketEvent.source == "finnhub",
                )
            )
            for e in all_events:
                session.add(MarketEvent(
                    country=e.country,
                    category="earnings" if "실적" in e.event_name else "macro",
                    event_name=e.event_name,
                    event_time=e.event_time,
                    importance=e.importance,
                    previous_value=e.previous_value,
                    forecast_value=e.forecast_value,
                    actual_value=e.actual_value,
                    source="finnhub",
                ))
            await session.commit()

        await cache_manager.set(
            events_key("week"),
            [
                {
                    "event_name": e.event_name,
                    "country": e.country,
                    "event_time": e.event_time.isoformat(),
                    "importance": e.importance,
                }
                for e in all_events
            ],
            ttl=TTL_EVENTS,
        )
        logger.info(f"Events updated: {len(all_events)} events")
    except Exception as e:
        logger.error(f"collect_events failed: {e}")


async def collect_indices() -> None:
    """지수/원자재 수집 → Redis."""
    try:
        yf = YfinanceCollector()
        kor_indices = await yf.collect_indices()

        async with FinnhubCollector() as fh:
            us_indices = await fh.collect_indices()

        summary = {}
        for idx in kor_indices:
            summary[idx.name] = {
                "price": idx.price,
                "change_percent": idx.change_percent,
            }
        for idx in us_indices:
            summary[idx.name] = {
                "price": idx.price,
                "change_percent": idx.change_percent,
            }

        await cache_manager.set(summary_bar_key(), summary, ttl=60)
        logger.info("Indices updated")
    except Exception as e:
        logger.error(f"collect_indices failed: {e}")


def setup_scheduler() -> AsyncIOScheduler:
    """스케줄 등록."""
    # 환율: 5분마다
    scheduler.add_job(collect_fx, "interval", minutes=5, id="fx", replace_existing=True)

    # 지수: 1분마다
    scheduler.add_job(collect_indices, "interval", minutes=1, id="indices", replace_existing=True)

    # 한국 시세: 1분마다 (내부에서 TTL 조절)
    scheduler.add_job(collect_kor_quotes, "interval", minutes=1, id="kor_quotes", replace_existing=True)

    # 미국 시세: 1분마다
    scheduler.add_job(collect_us_quotes, "interval", minutes=1, id="us_quotes", replace_existing=True)

    # 경제 일정: 30분마다
    scheduler.add_job(collect_events, "interval", minutes=30, id="events", replace_existing=True)

    return scheduler
