from datetime import datetime

from sqlalchemy import String, Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class FxRate(Base):
    __tablename__ = "fx_rates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pair: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)  # 예: USDKRW
    base_currency: Mapped[str] = mapped_column(String(3), nullable=False)       # 예: USD
    target_currency: Mapped[str] = mapped_column(String(3), nullable=False)     # 예: KRW
    rate: Mapped[float] = mapped_column(Float, nullable=False)
    prev_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    change_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
