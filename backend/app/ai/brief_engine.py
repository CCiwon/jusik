"""룰 매칭 + 문장 조합 엔진."""
import logging

from app.ai.snapshot_builder import MarketSnapshot
from app.ai.rules import OPENING_BRIEF_RULES

logger = logging.getLogger(__name__)

# 카테고리별 최대 선택 문장 수
_CATEGORY_LIMITS = {
    "market": 1,
    "sector": 1,
    "fx": 1,
    "event": 1,
}


def generate_opening_brief(snapshot: MarketSnapshot) -> list[str]:
    """매칭된 룰에서 최대 4개 문장을 선택하여 반환."""
    matched: list[tuple[int, str, str]] = []  # (priority, category, sentence)

    for rule in OPENING_BRIEF_RULES:
        try:
            if rule.condition(snapshot):
                sentence = rule.template(snapshot)
                matched.append((rule.priority, rule.category, sentence))
        except Exception as e:
            logger.warning(f"Rule '{rule.id}' failed: {e}")
            continue

    # 우선순위 내림차순 정렬
    matched.sort(key=lambda x: x[0], reverse=True)

    # 카테고리별 제한 적용
    category_counts: dict[str, int] = {}
    sentences: list[str] = []

    for priority, category, sentence in matched:
        limit = _CATEGORY_LIMITS.get(category, 1)
        if category_counts.get(category, 0) < limit:
            sentences.append(sentence)
            category_counts[category] = category_counts.get(category, 0) + 1

        if len(sentences) >= 4:
            break

    if not sentences:
        sentences = ["현재 시장 데이터를 바탕으로 브리프를 준비 중입니다."]

    return sentences
