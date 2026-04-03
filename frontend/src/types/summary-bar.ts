export interface IndexItem {
  name: string;
  price: number | null;
  change_percent: number | null;
}

export interface FxItem {
  pair: string;
  rate: number | null;
  change_percent: number | null;
}

export interface SummaryBarResponse {
  indices: IndexItem[];
  fx: FxItem[];
  updated_at: string | null;
}
