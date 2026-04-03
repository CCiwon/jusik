"""코스피 야간선물 / AP200 placeholder — KIS API 연결 예정."""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["futures"])


class FuturesItem(BaseModel):
    name: str
    price: float | None
    change_percent: float | None
    change_amount: float | None
    available: bool


class NightFuturesResponse(BaseModel):
    kospi_night_futures: FuturesItem
    ap200: FuturesItem
    note: str


@router.get("/futures/night", response_model=NightFuturesResponse)
async def night_futures():
    """코스피 야간선물 및 AP200 데이터 (KIS API 연결 전 placeholder)."""
    stub = FuturesItem(
        name="",
        price=None,
        change_percent=None,
        change_amount=None,
        available=False,
    )
    return NightFuturesResponse(
        kospi_night_futures=FuturesItem(**{**stub.model_dump(), "name": "KOSPI 야간선물"}),
        ap200=FuturesItem(**{**stub.model_dump(), "name": "AP200"}),
        note="KIS API 연결 필요",
    )
