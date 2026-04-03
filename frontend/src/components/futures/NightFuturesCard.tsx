"use client";

import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";

interface FuturesItem {
  name: string;
  price: number | null;
  change_percent: number | null;
  change_amount: number | null;
  available: boolean;
}

interface NightFuturesResponse {
  kospi_night_futures: FuturesItem;
  ap200: FuturesItem;
  note: string;
}

function FuturesRow({ item }: { item: FuturesItem }) {
  return (
    <div className="flex items-center justify-between py-1.5">
      <span className="text-slate-400 text-xs">{item.name}</span>
      {item.available ? (
        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="text-slate-200">{item.price?.toLocaleString() ?? "-"}</span>
          <span className={item.change_percent != null && item.change_percent >= 0 ? "text-green-400" : "text-red-400"}>
            {item.change_percent != null ? `${item.change_percent >= 0 ? "+" : ""}${item.change_percent.toFixed(2)}%` : "-"}
          </span>
        </div>
      ) : (
        <span className="text-slate-600 text-[10px]">KIS API 연결 예정</span>
      )}
    </div>
  );
}

export function NightFuturesCard() {
  const { data } = useQuery<NightFuturesResponse>({
    queryKey: ["futures", "night"],
    queryFn: async () => {
      const { data } = await apiClient.get<NightFuturesResponse>("/futures/night");
      return data;
    },
    staleTime: 60_000,
  });

  return (
    <div className="bg-slate-900 rounded-lg border border-slate-800 px-4 py-3">
      <h3 className="text-slate-400 text-xs font-medium mb-1">야간선물 · AP200</h3>
      {data ? (
        <div className="divide-y divide-slate-800">
          <FuturesRow item={data.kospi_night_futures} />
          <FuturesRow item={data.ap200} />
        </div>
      ) : (
        <div className="text-slate-600 text-xs py-2">데이터 없음</div>
      )}
    </div>
  );
}
