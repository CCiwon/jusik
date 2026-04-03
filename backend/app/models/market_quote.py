from datetime import datetime

from sqlalchemy import String, Float, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MarketQuote(Base):
    __tablename__ = "market_quotes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    instrument_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("instruments.id"), unique=True, nullable=False
    )
    price_local: Mapped[float | None] = mapped_column(Float, nullable=True)
    price_krw: Mapped[float | None] = mapped_column(Float, nullable=True)
    prev_close: Mapped[float | None] = mapped_column(Float, nullable=True)
    daily_change_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    daily_change_amount_local: Mapped[float | None] = mapped_column(Float, nullable=True)
    daily_change_amount_krw: Mapped[float | None] = mapped_column(Float, nullable=True)
    fx_impact_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    volume: Mapped[float | None] = mapped_column(Float, nullable=True)
    session_status: Mapped[str] = mapped_column(
        String(20), default="closed", nullable=False
    )
    # session_status: open | pre_market | after_market | closed
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    instrument: Mapped["Instrument"] = relationship(  # noqa: F821
        "Instrument", back_populates="quote"
    )
