from fastapi import APIRouter
from app.schemas.summary_bar import SummaryBarResponse
from app.services.summary_bar_service import get_summary_bar

router = APIRouter(prefix="/api", tags=["summary-bar"])


@router.get("/summary-bar", response_model=SummaryBarResponse)
async def summary_bar():
    return await get_summary_bar()
