type MetricCardProps = {
  title: string;
  value: string;
  delta: string;
};

export function MetricCard({
  title,
  value,
  delta,
}: MetricCardProps) {
  return (
    <article className="metric-card">
      <span>{title}</span>

      <h2>{value}</h2>

      <small>{delta}</small>
    </article>
  );
}