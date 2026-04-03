/** 등락률 포맷: +1.23% */
export function formatChange(v: number | null): string {
  if (v == null) return "-";
  return `${v >= 0 ? "+" : ""}${v.toFixed(2)}%`;
}

/** 원화 포맷: ₩1,234,567 */
export function formatKRW(v: number | null): string {
  if (v == null) return "-";
  return `₩${Math.round(v).toLocaleString("ko-KR")}`;
}

/** 달러 포맷: $123.45 */
export function formatUSD(v: number | null): string {
  if (v == null) return "-";
  return `$${v.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

/** 환율 포맷: 1,507.8 */
export function formatRate(v: number | null, digits = 1): string {
  if (v == null) return "-";
  return v.toLocaleString("ko-KR", { minimumFractionDigits: digits, maximumFractionDigits: digits });
}

/** 시가총액 포맷: 4,000억 / 40조 */
export function formatMarketCap(v: number | null, currency: "KRW" | "USD" = "KRW"): string {
  if (v == null) return "-";
  if (currency === "USD") {
    if (v >= 1_000_000) return `$${(v / 1_000_000).toFixed(1)}T`;
    if (v >= 1_000) return `$${(v / 1_000).toFixed(0)}B`;
    return `$${v}M`;
  }
  if (v >= 10_000) return `${(v / 10_000).toFixed(1)}조`;
  return `${v.toLocaleString()}억`;
}

/** 거래량 포맷: 1,234만 / 1.2억 */
export function formatVolume(v: number | null, isUS = false): string {
  if (v == null) return "-";
  if (isUS) {
    if (v >= 1_000_000) return `${(v / 1_000_000).toFixed(1)}M`;
    if (v >= 1_000) return `${(v / 1_000).toFixed(0)}K`;
    return v.toLocaleString();
  }
  if (v >= 100_000_000) return `${(v / 100_000_000).toFixed(1)}억`;
  if (v >= 10_000) return `${Math.round(v / 10_000)}만`;
  return v.toLocaleString();
}

/** 등락 색상 클래스 */
export function changeColor(v: number | null): string {
  if (v == null) return "text-slate-400";
  if (v > 0) return "text-green-400";
  if (v < 0) return "text-red-400";
  return "text-slate-400";
}

/** 히트맵 등락률 → 배경색 (red~green) */
export function heatmapColor(pct: number | null): string {
  if (pct == null) return "#1e293b";
  const clamped = Math.max(-5, Math.min(5, pct));
  if (clamped > 0) {
    const intensity = Math.round((clamped / 5) * 180);
    return `rgb(0, ${intensity + 60}, 0)`;
  }
  if (clamped < 0) {
    const intensity = Math.round((Math.abs(clamped) / 5) * 180);
    return `rgb(${intensity + 60}, 0, 0)`;
  }
  return "#334155";
}
