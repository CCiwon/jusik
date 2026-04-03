from pydantic import BaseModel


class SectorItem(BaseModel):
    sector_name: str
    sector_name_ko: str | None
    weighted_change_percent: float | None
    total_market_cap: float | None
    strongest_symbol: str | None
    weakest_symbol: str | None
    instruments: list[dict]   # {symbol, name, change_percent, market_cap}


class HeatmapResponse(BaseModel):
    KOR: list[SectorItem]
    US: list[SectorItem]
    top_sectors: list[str]
    bottom_sectors: list[str]
