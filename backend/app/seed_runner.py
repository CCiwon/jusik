"""DB 시드 데이터 적재 스크립트. 멱등성 보장 (upsert)."""
import asyncio
import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, Base, AsyncSessionLocal
from app.models.instrument import Instrument

SEED_DIR = Path(__file__).parent.parent / "seed"

# 기본 워치리스트 종목
DEFAULT_WATCHLIST = {
    "KOR": ["005930", "000660", "005380", "035420", "207940", "012450", "009540"],
    "US":  ["NVDA", "AAPL", "MSFT", "TSLA", "GOOGL", "META", "AMD"],
}


async def seed_instruments(session: AsyncSession, filepath: Path) -> int:
    data = json.loads(filepath.read_text())
    count = 0
    for item in data:
        market_type = item["market_type"]
        in_watchlist = item["symbol"] in DEFAULT_WATCHLIST.get(market_type, [])

        result = await session.execute(
            select(Instrument).where(
                Instrument.symbol == item["symbol"],
                Instrument.market_type == market_type,
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.company_name = item["company_name"]
            existing.company_name_ko = item.get("company_name_ko")
            existing.sector = item.get("sector")
            existing.market_cap = item.get("market_cap")
            existing.display_order = item.get("display_order", 999)
            # 이미 사용자가 수동으로 변경했을 수 있으니 덮어쓰지 않음
        else:
            session.add(
                Instrument(
                    symbol=item["symbol"],
                    company_name=item["company_name"],
                    company_name_ko=item.get("company_name_ko"),
                    market_type=market_type,
                    country=item["country"],
                    currency=item["currency"],
                    sector=item.get("sector"),
                    market_cap=item.get("market_cap"),
                    display_order=item.get("display_order", 999),
                    is_active=True,
                    in_watchlist=in_watchlist,
                )
            )
            count += 1

    await session.commit()
    return count


async def run() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        kor_count = await seed_instruments(session, SEED_DIR / "instruments_kor.json")
        us_count = await seed_instruments(session, SEED_DIR / "instruments_us.json")

    print(f"Seed complete — KOR: {kor_count} new, US: {us_count} new")


if __name__ == "__main__":
    asyncio.run(run())
