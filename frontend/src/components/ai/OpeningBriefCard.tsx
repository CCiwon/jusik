"use client";

import { useOpeningBrief } from "@/hooks/useOpeningBrief";
import { LoadingSkeleton } from "@/components/common/LoadingSkeleton";
import { ErrorFallback } from "@/components/common/ErrorFallback";

export function OpeningBriefCard() {
  const { data, isLoading, isError } = useOpeningBrief();

  return (
    <div className="bg-slate-900 rounded-lg border border-slate-800 h-full">
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="text-indigo-400 text-sm">✦</span>
          <h2 className="text-slate-200 text-sm font-semibold">개장 전 브리프</h2>
        </div>
        {data && (
          <span className="text-slate-500 text-[10px]">{data.generated_at}</span>
        )}
      </div>

      <div className="px-4 py-3">
        {isLoading && <LoadingSkeleton rows={3} />}
        {isError && <ErrorFallback />}
        {data && (
          <ul className="space-y-2">
            {data.sentences.map((sentence) => (
              <li key={sentence.slice(0, 30)} className="flex gap-2 text-xs text-slate-300 leading-relaxed">
                <span className="text-indigo-500 mt-0.5 shrink-0">·</span>
                <span>{sentence}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
