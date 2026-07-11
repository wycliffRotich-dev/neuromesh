import { ClusterHealth } from "../components/dashboard/ClusterHealth";
import { ResourceUsage } from "../components/dashboard/ResourceUsage";
import { StatCard } from "../components/dashboard/StatCard";
import { NodeTable } from "../components/nodes/NodeTable";
import { useNodes } from "../hooks/useNodes";

export default function DashboardPage() {
  const { nodes, loading, error } = useNodes();

  if (loading) {
    return (
      <main className="flex-1 p-8 text-white">
        Loading cluster...
      </main>
    );
  }

  if (error) {
    return (
      <main className="flex-1 p-8 text-red-400">
        {error}
      </main>
    );
  }

  const totalCpu = nodes.reduce(
    (sum, node) => sum + node.cpu_cores,
    0,
  );

  const totalMemory = nodes.reduce(
    (sum, node) => sum + node.memory_mib,
    0,
  );

  const totalVram = nodes.reduce(
    (sum, node) => sum + node.vram_mib,
    0,
  );

  return (
    <main className="flex-1 bg-slate-950 p-8">
      <h1 className="mb-8 text-3xl font-bold text-white">
        Dashboard
      </h1>

      <ClusterHealth nodes={nodes.length} />

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          title="Registered Nodes"
          value={nodes.length}
        />

        <StatCard
          title="CPU Cores"
          value={totalCpu}
        />

        <StatCard
          title="Memory (MiB)"
          value={totalMemory.toLocaleString()}
        />

        <StatCard
          title="VRAM (MiB)"
          value={totalVram.toLocaleString()}
        />
      </div>

      <ResourceUsage nodes={nodes} />

      <NodeTable nodes={nodes} />
    </main>
  );
}
