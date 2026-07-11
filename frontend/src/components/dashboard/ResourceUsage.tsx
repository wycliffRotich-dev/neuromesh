import { ProgressBar } from "./ProgressBar";
import type { NodeResponse } from "../../api/types";

type Props = {
  nodes: NodeResponse[];
};

export function ResourceUsage({ nodes }: Props) {
  const totalCpu = nodes.reduce(
    (sum, node) => sum + node.cpu_cores,
    0,
  );

  const availableCpu = nodes.reduce(
    (sum, node) => sum + node.available_cpu_cores,
    0,
  );

  const usedCpu = totalCpu - availableCpu;

  const totalMemory = nodes.reduce(
    (sum, node) => sum + node.memory_mib,
    0,
  );

  const availableMemory = nodes.reduce(
    (sum, node) => sum + node.available_memory_mib,
    0,
  );

  const usedMemory = totalMemory - availableMemory;

  const totalVram = nodes.reduce(
    (sum, node) => sum + node.vram_mib,
    0,
  );

  const availableVram = nodes.reduce(
    (sum, node) => sum + node.available_vram_mib,
    0,
  );

  const usedVram = totalVram - availableVram;

  return (
    <section className="mt-8 space-y-5">
      <ProgressBar
        label="CPU Usage"
        used={usedCpu}
        total={totalCpu}
        unit="cores"
      />

      <ProgressBar
        label="Memory Usage"
        used={usedMemory}
        total={totalMemory}
        unit="MiB"
      />

      <ProgressBar
        label="VRAM Usage"
        used={usedVram}
        total={totalVram}
        unit="MiB"
      />
    </section>
  );
}
