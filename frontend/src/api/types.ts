export interface NodeResponse {
  id: string;
  cpu_cores: number;
  memory_mib: number;
  vram_mib: number;
  available_cpu_cores: number;
  available_memory_mib: number;
  available_vram_mib: number;
}

export interface ListNodesResponse {
  nodes: NodeResponse[];
}