import { api } from "./client";
import type { ListNodesResponse } from "./types";

export function fetchNodes() {
  return api<ListNodesResponse>("/nodes");
}