export interface EventItem {
  id: number;
  country: string;
  category: string;
  event_name: string;
  event_name_ko: string | null;
  event_time: string;
  event_time_kst: string;
  importance: "high" | "medium" | "low";
  d_day: number;
  previous_value: string | null;
  forecast_value: string | null;
  actual_value: string | null;
}

export interface EventsResponse {
  items: EventItem[];
  total: number;
}

export type EventRange = "today" | "week" | "month";
export type EventCountry = "all" | "kor" | "us";
export type EventCategory = "all" | "macro" | "earnings" | "central_bank" | "policy";
