"use client";

import { useSummaryBar } from "@/hooks/useSummaryBar";
import { formatChange, formatRate, changeColor } from "@/lib/formatters";

const INDEX_LABELS: Record<string, string> = {
  KOSPI: "KOSPI",
  KOSDAQ: "KOSDAQ",
  SP500: "S&P500",
  NASDAQ100: "NASDAQ",
  DOW: "DOW",
  SOX: "SOX",
  WTI: "WTI",
  GOLD: "금",
  US10Y: "미10년물",
  VIX: "VIX",
};

const FX_LABELS: Record<string, string> = {
  USDKRW: "USD/KRW",
  JPYKRW: "JPY/KRW",
  EURKRW: "EUR/KRW",
};

export function SummaryBar() {
  const { data, isLoading } = useSummaryBar();

  if (isLoading || !data) {
    return (
      <div className="bg-slate-900 border-b border-slate-800 h-10 flex items-center px-4">
        <div className="h-4 w-full bg-slate-800 rounded animate-pulse" />
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border-b border-slate-800 sticky top-0 z-50">
      <div className="flex items-center gap-0 overflow-x-auto scrollbar-none px-2 h-10">
        {data.indices.map((item) => (
          <div
            key={item.name}
            className="flex items-center gap-1.5 px-3 py-1 border-r border-slate-800 shrink-0"
          >
            <span className="text-slate-400 text-xs">{INDEX_LABELS[item.name] ?? item.name}</span>
            <span className="text-slate-200 text-xs font-mono">
              {item.price != null
                ? item.name === "US10Y"
                  ? `${item.price.toFixed(2)}%`
                  : item.name === "VIX"
                  ? item.price.toFixed(2)
                  : item.price.toLocaleString()
                : "-"}
            </span>
            <span className={`text-xs font-mono ${changeColor(item.change_percent)}`}>
              {formatChange(item.change_percent)}
            </span>
          </div>
        ))}

        <div className="w-px h-6 bg-slate-700 mx-1 shrink-0" />

        {data.fx.map((item) => (
          <div
            key={item.pair}
            className="flex items-center gap-1.5 px-3 py-1 border-r border-slate-800 shrink-0"
          >
            <span className="text-slate-400 text-xs">{FX_LABELS[item.pair] ?? item.pair}</span>
            <span className="text-slate-200 text-xs font-mono">
              {formatRate(item.rate)}
            </span>
            <span className={`text-xs font-mono ${changeColor(item.change_percent)}`}>
              {formatChange(item.change_percent)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
