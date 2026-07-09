import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { resourceData } from "../data";

export function ResourceChart() {
  return (
    <section className="panel">
      <h2>Resource Usage</h2>

      <div style={{ width: "100%", height: 320 }}>
        <ResponsiveContainer>
          <LineChart data={resourceData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />

            <Line
              type="monotone"
              dataKey="cpu"
              stroke="#4f7cff"
            />

            <Line
              type="monotone"
              dataKey="memory"
              stroke="#22c55e"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}