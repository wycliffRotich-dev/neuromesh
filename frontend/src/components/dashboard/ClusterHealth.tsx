type Props = {
  nodes: number;
};

export function ClusterHealth({ nodes }: Props) {
  const healthy = true;

  return (
    <section className="mb-8 rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-lg">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white">
            Cluster Health
          </h2>

          <p className="mt-2 text-slate-400">
            Overall status of the NeuroMesh cluster
          </p>
        </div>

        <span
          className={`rounded-full px-4 py-2 text-sm font-semibold ${
            healthy
              ? "bg-emerald-500/20 text-emerald-400"
              : "bg-red-500/20 text-red-400"
          }`}
        >
          ● {healthy ? "Healthy" : "Offline"}
        </span>
      </div>

      <div className="mt-8 grid grid-cols-4 gap-6">
        <div className="rounded-xl bg-slate-800 p-5">
          <p className="text-sm text-slate-400">
            Nodes
          </p>

          <p className="mt-2 text-3xl font-bold text-white">
            {nodes}
          </p>
        </div>

        <div className="rounded-xl bg-slate-800 p-5">
          <p className="text-sm text-slate-400">
            Jobs
          </p>

          <p className="mt-2 text-3xl font-bold text-white">
            0
          </p>
        </div>

        <div className="rounded-xl bg-slate-800 p-5">
          <p className="text-sm text-slate-400">
            CPU Usage
          </p>

          <p className="mt-2 text-3xl font-bold text-emerald-400">
            0%
          </p>
        </div>

        <div className="rounded-xl bg-slate-800 p-5">
          <p className="text-sm text-slate-400">
            Memory
          </p>

          <p className="mt-2 text-3xl font-bold text-cyan-400">
            0 MiB
          </p>
        </div>
      </div>
    </section>
  );
}
