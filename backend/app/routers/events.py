from typing import Literal
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.event import EventsResponse
from app.services.event_service import get_events

router = APIRouter(prefix="/api", tags=["events"])


@router.get("/events", response_model=EventsResponse)
async def events(
    range: Literal["today", "week", "month"] = "week",
    country: Literal["all", "kor", "us"] = "all",
    category: Literal["all", "macro", "earnings", "central_bank", "policy"] = "all",
    session: AsyncSession = Depends(get_db),
):
    return await get_events(session, range_type=range, country=country, category=category)
