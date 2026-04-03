"use client";

import { useState } from "react";
import { useEvents } from "@/hooks/useEvents";
import type { EventRange, EventCountry } from "@/types";
import { LoadingSkeleton } from "../common/LoadingSkeleton";
import { ErrorFallback } from "../common/ErrorFallback";

const IMPORTANCE_STYLE: Record<string, string> = {
  high: "text-red-400 border-red-800",
  medium: "text-yellow-400 border-yellow-800",
  low: "text-slate-500 border-slate-700",
};

const COUNTRY_FLAG: Record<string, string> = {
  US: "🇺🇸",
  KOR: "🇰🇷",
};

function getEventLink(eventName: string, category: string, country: string): string | null {
  if (category === "earnings") {
    // "AAPL 실적 발표" → 심볼 추출
    const symbol = eventName.split(" ")[0];
    return `https://finance.yahoo.com/quote/${symbol}/`;
  }
  if (country === "KOR") {
    return `https://news.google.com/search?q=${encodeURIComponent(eventName)}&hl=ko`;
  }
  return `https://news.google.com/search?q=${encodeURIComponent(eventName)}&hl=en-US`;
}

export function EventBoard() {
  const [range, setRange] = useState<EventRange>("week");
  const [country, setCountry] = useState<EventCountry>("all");
  const { data, isLoading, isError } = useEvents({ range, country });

  return (
    <div className="bg-slate-900 rounded-lg border border-slate-800">
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800">
        <h2 className="text-slate-200 text-sm font-semibold">주요 일정</h2>
        <div className="flex items-center gap-2">
          <div className="flex rounded overflow-hidden border border-slate-700">
            {(["today", "week", "month"] as EventRange[]).map((r) => (
              <button
                key={r}
                onClick={() => setRange(r)}
                className={`px-2.5 py-1 text-xs transition-colors ${
                  range === r ? "bg-slate-600 text-white" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {r === "today" ? "오늘" : r === "week" ? "이번주" : "이번달"}
              </button>
            ))}
          </div>
          <div className="flex rounded overflow-hidden border border-slate-700">
            {(["all", "kor", "us"] as EventCountry[]).map((c) => (
              <button
                key={c}
                onClick={() => setCountry(c)}
                className={`px-2.5 py-1 text-xs transition-colors ${
                  country === c ? "bg-slate-600 text-white" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {c === "all" ? "전체" : c === "kor" ? "국장" : "미장"}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="divide-y divide-slate-800/60 max-h-96 overflow-y-auto">
        {isLoading && <div className="p-4"><LoadingSkeleton rows={5} /></div>}
        {isError && <ErrorFallback />}
        {data?.items.length === 0 && (
          <div className="text-center text-slate-500 text-sm py-8">
            해당 기간 일정이 없습니다
          </div>
        )}
        {data?.items.map((event) => (
          <div key={event.id} className="px-4 py-2.5 hover:bg-slate-800/40 transition-colors">
            <div className="flex items-start justify-between gap-2">
              <div className="flex items-start gap-2 min-w-0">
                <span className="text-base shrink-0 mt-0.5">
                  {COUNTRY_FLAG[event.country] ?? "🌐"}
                </span>
                <div className="min-w-0">
                  {getEventLink(event.event_name, event.category, event.country) ? (
                    <a
                      href={getEventLink(event.event_name, event.category, event.country)!}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-slate-200 text-xs font-medium truncate hover:text-blue-400 hover:underline transition-colors block"
                    >
                      {event.event_name}
                    </a>
                  ) : (
                    <div className="text-slate-200 text-xs font-medium truncate">
                      {event.event_name}
                    </div>
                  )}
                  <div className="text-slate-500 text-[10px] mt-0.5">
                    {event.event_time_kst}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                {event.d_day === 0 ? (
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-red-900/60 text-red-400 font-bold">
                    D-DAY
                  </span>
                ) : (
                  <span className="text-[10px] text-slate-500">D-{event.d_day}</span>
                )}
                <span
                  className={`text-[10px] px-1.5 py-0.5 rounded border ${
                    IMPORTANCE_STYLE[event.importance]
                  }`}
                >
                  {event.importance === "high" ? "높음" : event.importance === "medium" ? "중간" : "낮음"}
                </span>
              </div>
            </div>
            {(event.previous_value || event.forecast_value) && (
              <div className="mt-1 flex gap-3 text-[10px] text-slate-500 ml-6">
                {event.previous_value && <span>이전 {event.previous_value}</span>}
                {event.forecast_value && <span>예상 {event.forecast_value}</span>}
                {event.actual_value && (
                  <span className="text-yellow-400">실제 {event.actual_value}</span>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
