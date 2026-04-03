"""Redis 캐시 키 및 TTL 정의."""

# TTL (초)
TTL_FX = 5 * 60          # 환율: 5분
TTL_QUOTE = 60            # 시세: 1분
TTL_QUOTE_OFFHOURS = 30 * 60  # 장외 시세: 30분
TTL_SUMMARY_BAR = 60      # 상단 요약 바: 1분
TTL_SECTORS = 5 * 60      # 섹터: 5분
TTL_EVENTS = 30 * 60      # 일정: 30분


def fx_key(pair: str) -> str:
    """예: fx_key('USDKRW') -> 'fx:USDKRW'"""
    return f"fx:{pair}"


def quote_key(market: str, symbol: str) -> str:
    """예: quote_key('kor', '005930') -> 'quote:kor:005930'"""
    return f"quote:{market.lower()}:{symbol}"


def summary_bar_key() -> str:
    return "summary_bar"


def sectors_key(country: str) -> str:
    """예: sectors_key('KOR') -> 'sectors:KOR'"""
    return f"sectors:{country.upper()}"


def events_key(range_type: str, country: str = "all") -> str:
    """예: events_key('today', 'kor') -> 'events:today:kor'"""
    return f"events:{range_type}:{country.lower()}"


def ai_summary_key(summary_type: str, snapshot_hash: str) -> str:
    """예: ai_summary_key('opening_brief', 'abc123') -> 'ai:opening_brief:abc123'"""
    return f"ai:{summary_type}:{snapshot_hash}"


def kis_token_key() -> str:
    return "kis:access_token"
