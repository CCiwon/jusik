"use client";

import { useSectors } from "@/hooks/useSectors";
import { SectorTreemap } from "./SectorTreemap";
import { LoadingSkeleton } from "../common/LoadingSkeleton";
import { ErrorFallback } from "../common/ErrorFallback";
import { changeColor, formatChange } from "@/lib/formatters";

export function DualHeatmap() {
  const { data, isLoading, isError } = useSectors();

  if (isLoading) return (
    <div className="grid grid-cols-2 gap-4">
      <div className="bg-slate-900 rounded-lg border border-slate-800 p-3">
        <LoadingSkeleton rows={4} />
      </div>
      <div className="bg-slate-900 rounded-lg border border-slate-800 p-3">
        <LoadingSkeleton rows={4} />
      </div>
    </div>
  );

  if (isError || !data) return <ErrorFallback />;

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-4">
        <h2 className="text-slate-200 text-sm font-semibold">섹터 히트맵</h2>
        <div className="flex items-center gap-3 text-xs">
          <span className="text-slate-500">강세:</span>
          {data.top_sectors.slice(0, 3).map((s) => {
            const sector = [...data.KOR, ...data.US].find((x) => x.sector_name === s);
            return (
              <span key={s} className="text-green-400">
                {sector?.sector_name_ko ?? s} {formatChange(sector?.weighted_change_percent ?? null)}
              </span>
            );
          })}
          <span className="text-slate-500 ml-2">약세:</span>
          {data.bottom_sectors.slice(0, 3).map((s) => {
            const sector = [...data.KOR, ...data.US].find((x) => x.sector_name === s);
            return (
              <span key={s} className="text-red-400">
                {sector?.sector_name_ko ?? s} {formatChange(sector?.weighted_change_percent ?? null)}
              </span>
            );
          })}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <SectorTreemap sectors={data.KOR} title="국장 섹터" />
        <SectorTreemap sectors={data.US} title="미장 섹터" />
      </div>

      {/* 섹터 요약 바 */}
      <div className="grid grid-cols-2 gap-4">
        <div className="flex flex-wrap gap-1">
          {data.KOR.map((s) => (
            <span
              key={s.sector_name}
              className={`text-[10px] px-1.5 py-0.5 rounded border ${
                (s.weighted_change_percent ?? 0) >= 0
                  ? "border-green-800 text-green-400"
                  : "border-red-800 text-red-400"
              }`}
            >
              {s.sector_name_ko ?? s.sector_name} {formatChange(s.weighted_change_percent)}
            </span>
          ))}
        </div>
        <div className="flex flex-wrap gap-1">
          {data.US.map((s) => (
            <span
              key={s.sector_name}
              className={`text-[10px] px-1.5 py-0.5 rounded border ${
                (s.weighted_change_percent ?? 0) >= 0
                  ? "border-green-800 text-green-400"
                  : "border-red-800 text-red-400"
              }`}
            >
              {s.sector_name ?? s.sector_name} {formatChange(s.weighted_change_percent)}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
