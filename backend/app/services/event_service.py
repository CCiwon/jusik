"""경제 일정 서비스."""
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.market_event import MarketEvent
from app.schemas.event import EventItem, EventsResponse
from app.utils.timezone import to_kst, now_utc

KST = timezone(timedelta(hours=9))


async def get_events(
    session: AsyncSession,
    range_type: str = "week",
    country: str = "all",
    category: str = "all",
) -> EventsResponse:
    now = now_utc()

    if range_type == "today":
        end = now.replace(hour=23, minute=59, second=59)
    elif range_type == "month":
        end = now + timedelta(days=30)
    else:  # week
        end = now + timedelta(days=7)

    conditions = [
        MarketEvent.event_time >= now,
        MarketEvent.event_time <= end,
    ]
    if country != "all":
        conditions.append(MarketEvent.country == country.upper())
    if category != "all":
        conditions.append(MarketEvent.category == category)

    result = await session.execute(
        select(MarketEvent)
        .where(and_(*conditions))
        .order_by(MarketEvent.event_time)
        .limit(50)
    )
    events = result.scalars().all()

    items = []
    for e in events:
        event_time_kst = to_kst(e.event_time)
        d_day = (e.event_time.date() - now.date()).days

        items.append(EventItem(
            id=e.id,
            country=e.country,
            category=e.category,
            event_name=e.event_name,
            event_name_ko=e.event_name_ko,
            event_time=e.event_time,
            event_time_kst=event_time_kst.strftime("%m/%d %H:%M KST"),
            importance=e.importance,
            d_day=d_day,
            previous_value=e.previous_value,
            forecast_value=e.forecast_value,
            actual_value=e.actual_value,
        ))

    return EventsResponse(items=items, total=len(items))
