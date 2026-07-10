import { StatCard } from "../components/dashboard/StatCard";
import { NodeTable } from "../components/nodes/NodeTable";
import { useNodes } from "../hooks/useNodes";

export default function DashboardPage() {
  const { nodes, loading, error } = useNodes();

  if (loading) {
    return (
      <main className="flex-1 p-8">
        <h1 className="mb-8 text-3xl font-bold text-white">
          Dashboard
        </h1>

        <p className="text-gray-400">Loading cluster...</p>
      </main>
    );
  }

  if (error) {
    return (
      <main className="flex-1 p-8">
        <h1 className="mb-8 text-3xl font-bold text-white">
          Dashboard
        </h1>

        <p className="text-red-400">{error}</p>
      </main>
    );
  }

  return (
    <main className="flex-1 p-8">
      <h1 className="mb-8 text-3xl font-bold text-white">
        Dashboard
      </h1>

      <div className="mb-8 grid grid-cols-4 gap-6">
        <StatCard
          title="Nodes"
          value={nodes.length.toString()}
        />

        <StatCard title="Jobs" value="0" />
        <StatCard title="Running" value="0" />
        <StatCard title="GPU Utilization" value="0%" />
      </div>

      <NodeTable nodes={nodes} />
    </main>
  );
}
