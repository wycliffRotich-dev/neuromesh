interface StatCardProps {
  title: string;
  value: number | string;
}

export function StatCard({
  title,
  value,
}: StatCardProps) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900 p-6 shadow">
      <p className="text-sm text-slate-400">
        {title}
      </p>

      <h2 className="mt-3 text-3xl font-bold text-white">
        {value}
      </h2>
    </div>
  );
}