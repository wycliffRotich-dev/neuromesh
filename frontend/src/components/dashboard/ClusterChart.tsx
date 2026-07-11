import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { NodeResponse } from "../../api/types";
import { SectionCard } from "./SectionCard";

type Props = {
  nodes: NodeResponse[];
};

export function ClusterChart({ nodes }: Props) {
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

  const data = [
    {
      name: "CPU",
      used: totalCpu,
    },
    {
      name: "Memory",
      used: totalMemory,
    },
    {
      name: "VRAM",
      used: totalVram,
    },
  ];

  return (
    <SectionCard
      title="Cluster Resource Overview"
      subtitle="Aggregated cluster capacity"
    >
      <div className="h-72">
        <ResponsiveContainer
          width="100%"
          height="100%"
        >
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="name" />

            <YAxis />

            <Tooltip />

            <Area
              type="monotone"
              dataKey="used"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </SectionCard>
  );
}
