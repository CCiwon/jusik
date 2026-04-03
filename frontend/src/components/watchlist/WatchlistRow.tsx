import type { WatchlistItem } from "@/types";
import { changeColor, formatChange, formatKRW, formatUSD, formatVolume } from "@/lib/formatters";
import { useToggleWatchlist } from "@/hooks/useWatchlistMutations";

interface Props {
  item: WatchlistItem;
}

export function WatchlistRow({ item }: Props) {
  const name = item.company_name_ko ?? item.company_name;
  const isUS = item.market_type === "US";
  const isOpen = item.session_status === "open";
  const toggle = useToggleWatchlist();

  return (
    <tr className="border-b border-slate-800/60 hover:bg-slate-800/40 transition-colors group">
      <td className="px-4 py-2.5">
        <div className="flex items-center gap-2">
          <span
            className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${
              isUS ? "bg-blue-900/60 text-blue-300" : "bg-rose-900/60 text-rose-300"
            }`}
          >
            {item.market_type}
          </span>
          <div>
            <div className="text-slate-200 font-medium">{name}</div>
            <div className="text-slate-500 text-[10px]">{item.symbol}</div>
          </div>
        </div>
      </td>

      <td className="px-3 py-2.5 text-right">
        <span className="text-slate-200 font-mono">
          {isUS ? formatUSD(item.price_local) : formatKRW(item.price_local)}
        </span>
      </td>

      <td className="px-3 py-2.5 text-right">
        <span className={`font-mono ${changeColor(item.daily_change_percent)}`}>
          {formatChange(item.daily_change_percent)}
        </span>
      </td>

      <td className="px-3 py-2.5 text-right hidden sm:table-cell">
        {isUS ? (
          <span className="text-yellow-300/90 font-mono text-xs">
            {formatKRW(item.price_krw)}
          </span>
        ) : (
          <span className="text-slate-500 text-xs">-</span>
        )}
      </td>

      <td className="px-3 py-2.5 text-right hidden md:table-cell">
        {isUS && item.daily_change_amount_krw != null ? (
          <div>
            <div className={`font-mono text-xs ${changeColor(item.daily_change_amount_krw)}`}>
              {item.daily_change_amount_krw >= 0 ? "+" : ""}
              {formatKRW(item.daily_change_amount_krw)}
            </div>
            {item.fx_impact_percent != null && (
              <div className={`font-mono text-[10px] ${changeColor(item.fx_impact_percent)}`}>
                환율 {item.fx_impact_percent >= 0 ? "+" : ""}{item.fx_impact_percent.toFixed(2)}%p
              </div>
            )}
          </div>
        ) : (
          <span className="text-slate-500 text-xs">-</span>
        )}
      </td>

      <td className="px-3 py-2.5 text-right hidden lg:table-cell">
        <span className="text-slate-500 font-mono text-xs">
          {formatVolume(item.volume, isUS)}
        </span>
      </td>

      <td className="px-3 py-2.5 text-center hidden lg:table-cell">
        <span
          className={`text-[10px] px-1.5 py-0.5 rounded ${
            isOpen ? "bg-green-900/50 text-green-400" : "text-slate-600"
          }`}
        >
          {isOpen ? "장중" : "마감"}
        </span>
      </td>

      <td className="px-2 py-2.5 text-center">
        <button
          onClick={() => toggle.mutate({ marketType: item.market_type, symbol: item.symbol })}
          disabled={toggle.isPending}
          className="opacity-0 group-hover:opacity-100 text-slate-600 hover:text-red-400 transition-all text-base leading-none px-1"
          title="워치리스트에서 제거"
        >
          ×
        </button>
      </td>
    </tr>
  );
}
