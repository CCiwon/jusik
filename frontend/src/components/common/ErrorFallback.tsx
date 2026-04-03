interface Props {
  message?: string;
}

export function ErrorFallback({ message = "데이터를 불러올 수 없습니다" }: Props) {
  return (
    <div className="flex items-center justify-center h-24 text-slate-500 text-sm">
      {message}
    </div>
  );
}
