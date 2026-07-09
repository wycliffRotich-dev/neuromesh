import { api } from "./client";
import type { DashboardResponse } from "./types";

export function fetchDashboard() {
  return api<DashboardResponse>("/api/dashboard");
}