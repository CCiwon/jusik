from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.sector import HeatmapResponse
from app.services.sector_service import get_heatmap

router = APIRouter(prefix="/api/sectors", tags=["sectors"])


@router.get("/heatmap", response_model=HeatmapResponse)
async def heatmap(session: AsyncSession = Depends(get_db)):
    return await get_heatmap(session)
