"""AI 개장 전 브리프 서비스."""
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.snapshot_builder import build_snapshot, compute_snapshot_hash
from app.ai.brief_engine import generate_opening_brief
from app.cache.cache_keys import ai_summary_key
from app.cache.cache_manager import cache_manager
from app.models.ai_summary import AiSummary
from app.schemas.ai_brief import OpeningBriefResponse

KST = timezone(timedelta(hours=9))
TTL_AI_BRIEF = 30 * 60


def _now_kst_str() -> str:
    return datetime.now(KST).strftime("%Y-%m-%d %H:%M KST")


async def get_opening_brief(session: AsyncSession) -> OpeningBriefResponse:
    snapshot = await build_snapshot(session)
    snapshot_hash = compute_snapshot_hash(snapshot)
    cache_key = ai_summary_key("opening_brief", snapshot_hash)

    cached_data = await cache_manager.get(cache_key)
    if cached_data:
        return OpeningBriefResponse(**cached_data, cached=True)

    sentences = generate_opening_brief(snapshot)
    content = " ".join(sentences)
    generated_at = _now_kst_str()

    response = OpeningBriefResponse(
        sentences=sentences,
        content=content,
        generated_at=generated_at,
        snapshot_hash=snapshot_hash,
        cached=False,
    )

    await cache_manager.set(
        cache_key,
        {"sentences": sentences, "content": content, "generated_at": generated_at, "snapshot_hash": snapshot_hash},
        ttl=TTL_AI_BRIEF,
    )

    try:
        session.add(AiSummary(
            summary_type="opening_brief",
            input_snapshot_hash=snapshot_hash,
            content=content,
        ))
        await session.commit()
    except Exception as e:
        await session.rollback()
        logger.error(f"Failed to persist AI brief: {e}")

    return response
