import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { SectionCard } from "./SectionCard";

const data = [
  {
    name: "CPU",
    used: 18,
  },
  {
    name: "Memory",
    used: 62,
  },
  {
    name: "VRAM",
    used: 34,
  },
];

export function ClusterChart() {
  return (
    <SectionCard
      title="Cluster Resource Overview"
      subtitle="Current cluster utilization"
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
