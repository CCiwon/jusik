import { SummaryBar } from "@/components/layout/SummaryBar";
import { WatchlistBoard } from "@/components/watchlist/WatchlistBoard";
import { DualHeatmap } from "@/components/heatmap/DualHeatmap";
import { EventBoard } from "@/components/events/EventBoard";
import { OpeningBriefCard } from "@/components/ai/OpeningBriefCard";
import { NightFuturesCard } from "@/components/futures/NightFuturesCard";

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-[#0f1117]">
      <SummaryBar />

      <main className="max-w-[1600px] mx-auto px-4 py-4 space-y-4">
        {/* Section 1: AI 브리프 + 야간선물 + 이벤트 */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
          <div className="xl:col-span-2 flex flex-col gap-4">
            <OpeningBriefCard />
            <NightFuturesCard />
          </div>
          <div>
            <EventBoard />
          </div>
        </div>

        {/* Section 2: 관심종목 */}
        <WatchlistBoard />

        {/* Section 3: 듀얼 히트맵 */}
        <DualHeatmap />
      </main>
    </div>
  );
}
