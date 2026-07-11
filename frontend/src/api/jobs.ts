import { api } from "./client";

export type CreateJobRequest = {
  cpu_cores: number;
  memory_mib: number;
  vram_mib: number;
};

export function createJob(
  job: CreateJobRequest,
) {
  return api(
    "/jobs",
    {
      method: "POST",
      body: JSON.stringify(job),
    },
  );
}
