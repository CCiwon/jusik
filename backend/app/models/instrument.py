from sqlalchemy import String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Instrument(Base):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    company_name: Mapped[str] = mapped_column(String(100), nullable=False)
    company_name_ko: Mapped[str | None] = mapped_column(String(100), nullable=True)
    market_type: Mapped[str] = mapped_column(String(5), nullable=False)   # KOR | US
    country: Mapped[str] = mapped_column(String(5), nullable=False)       # KR | US
    currency: Mapped[str] = mapped_column(String(3), nullable=False)      # KRW | USD
    sector: Mapped[str | None] = mapped_column(String(50), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(100), nullable=True)
    market_cap: Mapped[float | None] = mapped_column(Float, nullable=True)  # 억 단위
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    in_watchlist: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(default=999, nullable=False)

    quote: Mapped["MarketQuote | None"] = relationship(  # noqa: F821
        "MarketQuote", back_populates="instrument", uselist=False
    )

    def __repr__(self) -> str:
        return f"<Instrument {self.market_type}:{self.symbol}>"
