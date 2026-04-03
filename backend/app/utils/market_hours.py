"""KST 기준 시장 개장 상태 판별."""
from datetime import datetime, time
import pytz

KST = pytz.timezone("Asia/Seoul")
EST = pytz.timezone("America/New_York")

# 한국장: 09:00 ~ 15:30 KST (월~금)
KOR_OPEN = time(9, 0)
KOR_CLOSE = time(15, 30)

# 미국장: 09:30 ~ 16:00 ET → KST 변환 시 여름 22:30~05:00, 겨울 23:30~06:00
# 단순화: KST 기준 22:00 ~ 06:00 로 처리
US_OPEN_KST = time(22, 0)
US_CLOSE_KST = time(6, 0)


def now_kst() -> datetime:
    return datetime.now(KST)


def is_weekday(dt: datetime) -> bool:
    return dt.weekday() < 5  # 0=월 ~ 4=금


def is_kor_market_open() -> bool:
    now = now_kst()
    if not is_weekday(now):
        return False
    return KOR_OPEN <= now.time() <= KOR_CLOSE


def is_us_market_open() -> bool:
    """KST 기준 22:00 이후 또는 06:00 이전 (자정 넘어감)."""
    now = now_kst()
    if not is_weekday(now):
        return False
    t = now.time()
    return t >= US_OPEN_KST or t <= US_CLOSE_KST


def get_quote_ttl(market: str) -> int:
    """시장별 현재 적절한 캐시 TTL(초) 반환."""
    if market == "KOR":
        return 60 if is_kor_market_open() else 30 * 60
    if market == "US":
        return 60 if is_us_market_open() else 30 * 60
    return 60


def get_fx_ttl() -> int:
    """환율 TTL — 장중이면 5분, 장외면 30분."""
    if is_kor_market_open() or is_us_market_open():
        return 5 * 60
    return 30 * 60


def get_session_status(market: str) -> str:
    """open | closed"""
    if market == "KOR":
        return "open" if is_kor_market_open() else "closed"
    if market == "US":
        return "open" if is_us_market_open() else "closed"
    return "closed"
