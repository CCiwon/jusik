from pydantic import BaseModel
from datetime import datetime


class EventItem(BaseModel):
    id: int
    country: str
    category: str
    event_name: str
    event_name_ko: str | None
    event_time: datetime
    event_time_kst: str
    importance: str
    d_day: int
    previous_value: str | None
    forecast_value: str | None
    actual_value: str | None


class EventsResponse(BaseModel):
    items: list[EventItem]
    total: int
