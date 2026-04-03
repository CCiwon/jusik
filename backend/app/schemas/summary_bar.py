from pydantic import BaseModel


class IndexItem(BaseModel):
    name: str
    price: float | None
    change_percent: float | None


class FxItem(BaseModel):
    pair: str
    rate: float | None
    change_percent: float | None


class SummaryBarResponse(BaseModel):
    indices: list[IndexItem]
    fx: list[FxItem]
    updated_at: str | None = None
