"use client";

import { useState } from "react";
import { useWatchlist } from "@/hooks/useWatchlist";
import type { MarketFilter, WatchlistSortKey } from "@/types";
import { WatchlistRow } from "./WatchlistRow";
import { AddInstrumentModal } from "./AddInstrumentModal";
import { LoadingSkeleton } from "../common/LoadingSkeleton";
import { ErrorFallback } from "../common/ErrorFallback";

const SORT_OPTIONS: { label: string; value: WatchlistSortKey }[] = [
  { label: "기본순", value: "display_order" },
  { label: "등락률", value: "change" },
  { label: "원화변화", value: "krw_delta" },
  { label: "시총", value: "market_cap" },
];

const MARKET_OPTIONS: { label: string; value: MarketFilter }[] = [
  { label: "전체", value: "all" },
  { label: "국장", value: "kor" },
  { label: "미장", value: "us" },
];

export function WatchlistBoard() {
  const [market, setMarket] = useState<MarketFilter>("all");
  const [sort, setSort] = useState<WatchlistSortKey>("display_order");
  const [modalOpen, setModalOpen] = useState(false);
  const { data, isLoading, isError } = useWatchlist({ market, sort });

  return (
    <div className="bg-slate-900 rounded-lg border border-slate-800">
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800">
        <h2 className="text-slate-200 text-sm font-semibold">관심종목</h2>
        <div className="flex items-center gap-2">
          <div className="flex rounded overflow-hidden border border-slate-700">
            {MARKET_OPTIONS.map((opt) => (
              <button
                key={opt.value}
                onClick={() => setMarket(opt.value)}
                className={`px-2.5 py-1 text-xs transition-colors ${
                  market === opt.value
                    ? "bg-slate-600 text-white"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {opt.label}
              </button>
            ))}
          </div>
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value as WatchlistSortKey)}
            className="bg-slate-800 text-slate-300 text-xs px-2 py-1 rounded border border-slate-700 outline-none"
          >
            {SORT_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
          {data?.usdkrw && (
            <span className="text-slate-500 text-xs">
              USD/KRW {data.usdkrw.toLocaleString()}
            </span>
          )}
          <button
            onClick={() => setModalOpen(true)}
            className="text-slate-400 hover:text-slate-200 border border-slate-700 hover:border-slate-500 rounded px-2 py-1 text-xs transition-colors"
          >
            + 추가
          </button>
        </div>
      </div>
      {modalOpen && <AddInstrumentModal onClose={() => setModalOpen(false)} />}

      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr className="text-slate-500 border-b border-slate-800">
              <th className="text-left px-4 py-2 font-normal">종목</th>
              <th className="text-right px-3 py-2 font-normal">현재가</th>
              <th className="text-right px-3 py-2 font-normal">등락률</th>
              <th className="text-right px-3 py-2 font-normal hidden sm:table-cell">원화환산</th>
              <th className="text-right px-3 py-2 font-normal hidden md:table-cell">원화변화</th>
              <th className="text-right px-3 py-2 font-normal hidden lg:table-cell">거래량</th>
              <th className="text-center px-3 py-2 font-normal hidden lg:table-cell">상태</th>
              <th className="px-2 py-2" />
            </tr>
          </thead>
          <tbody>
            {isLoading && (
              <tr>
                <td colSpan={7} className="px-4 py-4">
                  <LoadingSkeleton rows={8} />
                </td>
              </tr>
            )}
            {isError && (
              <tr>
                <td colSpan={7}>
                  <ErrorFallback />
                </td>
              </tr>
            )}
            {data?.items.map((item) => (
              <WatchlistRow key={`${item.market_type}-${item.symbol}`} item={item} />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
