import { changeColor, formatChange } from "@/lib/formatters";

interface Props {
  value: number | null;
  className?: string;
}

export function ChangeIndicator({ value, className = "" }: Props) {
  return (
    <span className={`font-mono text-sm ${changeColor(value)} ${className}`}>
      {formatChange(value)}
    </span>
  );
}
