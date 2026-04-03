from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.ai_brief import OpeningBriefResponse
from app.services.ai_brief_service import get_opening_brief

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.get("/opening-brief", response_model=OpeningBriefResponse)
async def opening_brief(session: AsyncSession = Depends(get_db)):
    return await get_opening_brief(session)
