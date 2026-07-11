import { useState } from "react";

import { createJob } from "../../api/jobs";

type Props = {
  onSubmitted: () => void;
};

export function SubmitJobForm({
  onSubmitted,
}: Props) {
  const [cpu, setCpu] = useState(1);
  const [memory, setMemory] = useState(2048);
  const [vram, setVram] = useState(0);

  const [loading, setLoading] =
    useState(false);

  async function submit(
    e: React.FormEvent,
  ) {
    e.preventDefault();

    setLoading(true);

    try {
      await createJob({
        cpu_cores: cpu,
        memory_mib: memory,
        vram_mib: vram,
      });

      onSubmitted();
    } catch (err) {
      alert(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="rounded-xl border border-slate-700 bg-slate-900 p-6">
      <h2 className="mb-6 text-xl font-semibold text-white">
        Submit Job
      </h2>

      <form
        onSubmit={submit}
        className="space-y-4"
      >
        <div>
          <label className="mb-2 block text-sm text-slate-300">
            CPU Cores
          </label>

          <input
            type="number"
            value={cpu}
            onChange={(e) =>
              setCpu(Number(e.target.value))
            }
            className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white"
          />
        </div>

        <div>
          <label className="mb-2 block text-sm text-slate-300">
            Memory (MiB)
          </label>

          <input
            type="number"
            value={memory}
            onChange={(e) =>
              setMemory(Number(e.target.value))
            }
            className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white"
          />
        </div>

        <div>
          <label className="mb-2 block text-sm text-slate-300">
            VRAM (MiB)
          </label>

          <input
            type="number"
            value={vram}
            onChange={(e) =>
              setVram(Number(e.target.value))
            }
            className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white"
          />
        </div>

        <button
          disabled={loading}
          className="rounded bg-indigo-600 px-5 py-2 text-white hover:bg-indigo-500 disabled:opacity-50"
        >
          {loading
            ? "Submitting..."
            : "Submit Job"}
        </button>
      </form>
    </section>
  );
}
