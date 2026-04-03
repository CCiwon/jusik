from datetime import datetime

from sqlalchemy import String, Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SectorSnapshot(Base):
    __tablename__ = "sector_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    country: Mapped[str] = mapped_column(String(5), nullable=False)       # KOR | US
    sector_name: Mapped[str] = mapped_column(String(50), nullable=False)
    sector_name_ko: Mapped[str | None] = mapped_column(String(50), nullable=True)
    weighted_change_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    total_market_cap: Mapped[float | None] = mapped_column(Float, nullable=True)
    strongest_symbol: Mapped[str | None] = mapped_column(String(20), nullable=True)
    weakest_symbol: Mapped[str | None] = mapped_column(String(20), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
