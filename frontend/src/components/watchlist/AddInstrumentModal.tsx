"use client";

import { useState, useEffect, useRef } from "react";
import { apiClient } from "@/lib/api-client";
import { useToggleWatchlist } from "@/hooks/useWatchlistMutations";
import type { InstrumentSearchItem } from "@/types";

interface Props {
  onClose: () => void;
}

export function AddInstrumentModal({ onClose }: Props) {
  const [query, setQuery] = useState("");
  const [market, setMarket] = useState<"all" | "kor" | "us">("all");
  const [results, setResults] = useState<InstrumentSearchItem[]>([]);
  const [loading, setLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const toggle = useToggleWatchlist();

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }
    const timer = setTimeout(async () => {
      setLoading(true);
      try {
        const { data } = await apiClient.get("/instruments/search", {
          params: { q: query, market },
        });
        setResults(data);
      } finally {
        setLoading(false);
      }
    }, 300);
    return () => clearTimeout(timer);
  }, [query, market]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-md mx-4 shadow-2xl">
        <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800">
          <h3 className="text-slate-200 text-sm font-semibold">종목 추가</h3>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-lg leading-none">×</button>
        </div>

        <div className="p-4 space-y-3">
          <div className="flex gap-2">
            <input
              ref={inputRef}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="종목명 또는 심볼 검색..."
              className="flex-1 bg-slate-800 text-slate-200 text-sm px-3 py-2 rounded-lg border border-slate-700 outline-none focus:border-slate-500 placeholder-slate-500"
            />
            <select
              value={market}
              onChange={(e) => setMarket(e.target.value as "all" | "kor" | "us")}
              className="bg-slate-800 text-slate-300 text-sm px-2 py-2 rounded-lg border border-slate-700 outline-none"
            >
              <option value="all">전체</option>
              <option value="kor">국장</option>
              <option value="us">미장</option>
            </select>
          </div>

          <div className="space-y-1 max-h-72 overflow-y-auto">
            {loading && (
              <div className="text-center text-slate-500 text-sm py-4">검색 중...</div>
            )}
            {!loading && query && results.length === 0 && (
              <div className="text-center text-slate-500 text-sm py-4">검색 결과 없음</div>
            )}
            {!loading && !query && (
              <div className="text-center text-slate-600 text-sm py-4">종목명 또는 심볼을 입력하세요</div>
            )}
            {results.map((item) => (
              <div
                key={`${item.market_type}-${item.symbol}`}
                className="flex items-center justify-between px-3 py-2.5 rounded-lg hover:bg-slate-800 transition-colors"
              >
                <div className="flex items-center gap-2">
                  <span
                    className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${
                      item.market_type === "US"
                        ? "bg-blue-900/60 text-blue-300"
                        : "bg-rose-900/60 text-rose-300"
                    }`}
                  >
                    {item.market_type}
                  </span>
                  <div>
                    <div className="text-slate-200 text-sm">
                      {item.company_name_ko ?? item.company_name}
                    </div>
                    <div className="text-slate-500 text-xs">{item.symbol} · {item.sector}</div>
                  </div>
                </div>
                <button
                  onClick={() => toggle.mutate({ marketType: item.market_type, symbol: item.symbol })}
                  disabled={toggle.isPending}
                  className={`text-xs px-3 py-1 rounded-lg border transition-colors ${
                    item.in_watchlist
                      ? "border-red-700 text-red-400 hover:bg-red-900/30"
                      : "border-green-700 text-green-400 hover:bg-green-900/30"
                  }`}
                >
                  {item.in_watchlist ? "제거" : "추가"}
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
