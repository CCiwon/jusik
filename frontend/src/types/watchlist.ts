export interface WatchlistItem {
  symbol: string;
  company_name: string;
  company_name_ko: string | null;
  market_type: "KOR" | "US";
  sector: string | null;
  price_local: number | null;
  currency: string;
  price_krw: number | null;
  daily_change_percent: number | null;
  daily_change_amount_local: number | null;
  daily_change_amount_krw: number | null;
  session_status: "open" | "closed" | "pre_market" | "after_market";
  market_cap: number | null;
  volume: number | null;
  fx_impact_percent: number | null;
}

export interface WatchlistResponse {
  items: WatchlistItem[];
  usdkrw: number | null;
}

export interface InstrumentSearchItem {
  symbol: string;
  company_name: string;
  company_name_ko: string | null;
  market_type: "KOR" | "US";
  sector: string | null;
  in_watchlist: boolean;
}

export type WatchlistSortKey = "display_order" | "change" | "krw_delta" | "market_cap";
export type MarketFilter = "all" | "kor" | "us";
