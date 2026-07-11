type Props = {
  label: string;
  used: number;
  total: number;
  unit: string;
};

export function ProgressBar({
  label,
  used,
  total,
  unit,
}: Props) {
  const percentage =
    total === 0 ? 0 : Math.min((used / total) * 100, 100);

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
      <div className="mb-3 flex items-center justify-between">
        <span className="font-medium text-slate-300">
          {label}
        </span>

        <span className="text-sm text-slate-400">
          {used.toLocaleString()} / {total.toLocaleString()} {unit}
        </span>
      </div>

      <div className="h-3 overflow-hidden rounded-full bg-slate-800">
        <div
          className="h-full rounded-full bg-cyan-500 transition-all duration-500"
          style={{
            width: `${percentage}%`,
          }}
        />
      </div>

      <div className="mt-2 text-right text-sm text-cyan-400">
        {percentage.toFixed(1)}%
      </div>
    </div>
  );
}
