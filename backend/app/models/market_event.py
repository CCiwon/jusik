from datetime import datetime

from sqlalchemy import String, Float, DateTime, func, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MarketEvent(Base):
    __tablename__ = "market_events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    country: Mapped[str] = mapped_column(String(5), nullable=False)        # KOR | US
    category: Mapped[str] = mapped_column(String(20), nullable=False)
    # category: macro | earnings | central_bank | tech | policy
    event_name: Mapped[str] = mapped_column(String(200), nullable=False)
    event_name_ko: Mapped[str | None] = mapped_column(String(200), nullable=True)
    event_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    importance: Mapped[str] = mapped_column(String(10), default="medium", nullable=False)
    # importance: high | medium | low
    previous_value: Mapped[str | None] = mapped_column(String(50), nullable=True)
    forecast_value: Mapped[str | None] = mapped_column(String(50), nullable=True)
    actual_value: Mapped[str | None] = mapped_column(String(50), nullable=True)
    related_assets: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON 문자열
    source: Mapped[str | None] = mapped_column(String(50), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
