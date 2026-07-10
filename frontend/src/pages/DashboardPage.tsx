import { StatCard } from "../components/dashboard/StatCard";

export default function DashboardPage() {
  return (
    <main className="flex-1 p-8">
      <h1 className="mb-8 text-3xl font-bold text-white">
        Dashboard
      </h1>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          title="Registered Nodes"
          value={0}
        />

        <StatCard
          title="CPU Cores"
          value={0}
        />

        <StatCard
          title="Memory (MiB)"
          value={0}
        />

        <StatCard
          title="VRAM (MiB)"
          value={0}
        />
      </div>
    </main>
  );
}
