export interface SectorInstrument {
  symbol: string;
  name: string;
  change_percent: number | null;
  market_cap: number | null;
}

export interface SectorItem {
  sector_name: string;
  sector_name_ko: string | null;
  weighted_change_percent: number | null;
  total_market_cap: number | null;
  strongest_symbol: string | null;
  weakest_symbol: string | null;
  instruments: SectorInstrument[];
}

export interface HeatmapResponse {
  KOR: SectorItem[];
  US: SectorItem[];
  top_sectors: string[];
  bottom_sectors: string[];
}
