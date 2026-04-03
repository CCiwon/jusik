"""시간대 변환 유틸 — 모든 저장은 UTC, 표시는 KST."""
from datetime import datetime
import pytz

KST = pytz.timezone("Asia/Seoul")
UTC = pytz.utc


def to_kst(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = UTC.localize(dt)
    return dt.astimezone(KST)


def to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = KST.localize(dt)
    return dt.astimezone(UTC)


def now_utc() -> datetime:
    return datetime.now(UTC)


def now_kst() -> datetime:
    return datetime.now(KST)
