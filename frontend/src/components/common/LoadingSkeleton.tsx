interface Props {
  rows?: number;
  className?: string;
}

export function LoadingSkeleton({ rows = 5, className = "" }: Props) {
  return (
    <div className={`space-y-2 ${className}`}>
      {Array.from({ length: rows }).map((_, i) => (
        <div
          key={i}
          className="h-8 bg-slate-800 rounded animate-pulse"
          style={{ opacity: 1 - i * 0.15 }}
        />
      ))}
    </div>
  );
}
