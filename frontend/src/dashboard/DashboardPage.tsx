import { ClusterOverview } from "./components/ClusterOverview";
import { MetricCard } from "./components/MetricCard";
import { ResourceChart } from "./components/ResourceChart";
import { metrics } from "./data";

export function DashboardPage() {
  return (
    <>
      <section className="metrics-grid">
        {metrics.map((metric) => (
          <MetricCard
            key={metric.title}
            title={metric.title}
            value={metric.value}
            delta={metric.delta}
          />
        ))}
      </section>

      <section className="dashboard-grid">
        <ClusterOverview />

        <ResourceChart />
      </section>
    </>
  );
}