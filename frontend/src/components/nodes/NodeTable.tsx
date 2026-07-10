import type { NodeResponse } from "../../api/types";

type Props = {
  nodes: NodeResponse[];
};

export function NodeTable({ nodes }: Props) {
  return (
    <section className="mt-10 overflow-hidden rounded-xl border border-slate-700 bg-slate-900">
      <div className="border-b border-slate-700 px-6 py-4">
        <h2 className="text-xl font-semibold text-white">
          Cluster Nodes
        </h2>
      </div>

      <table className="w-full">
        <thead className="bg-slate-800 text-left text-sm text-slate-300">
          <tr>
            <th className="px-6 py-3">Node ID</th>
            <th className="px-6 py-3">CPU</th>
            <th className="px-6 py-3">Available CPU</th>
            <th className="px-6 py-3">Memory (MiB)</th>
            <th className="px-6 py-3">VRAM (MiB)</th>
          </tr>
        </thead>

        <tbody>
          {nodes.length === 0 ? (
            <tr>
              <td
                colSpan={5}
                className="px-6 py-10 text-center text-slate-400"
              >
                No compute nodes have been registered.
              </td>
            </tr>
          ) : (
            nodes.map((node) => (
              <tr
                key={node.id}
                className="border-t border-slate-800 hover:bg-slate-800/40"
              >
                <td className="px-6 py-4 font-mono text-sm text-white">
                  {node.id}
                </td>

                <td className="px-6 py-4 text-slate-200">
                  {node.cpu_cores}
                </td>

                <td className="px-6 py-4 text-emerald-400">
                  {node.available_cpu_cores}
                </td>

                <td className="px-6 py-4 text-slate-200">
                  {node.memory_mib.toLocaleString()}
                </td>

                <td className="px-6 py-4 text-slate-200">
                  {node.vram_mib.toLocaleString()}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </section>
  );
}
