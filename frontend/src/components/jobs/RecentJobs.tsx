type Job = {
  id: string;
  name: string;
  status: "Running" | "Queued" | "Completed" | "Failed";
  node: string;
};

type Props = {
  jobs: Job[];
};

const badgeStyles = {
  Running: "bg-green-500/20 text-green-400",
  Queued: "bg-yellow-500/20 text-yellow-400",
  Completed: "bg-blue-500/20 text-blue-400",
  Failed: "bg-red-500/20 text-red-400",
};

export function RecentJobs({ jobs }: Props) {
  return (
    <section className="mt-8 rounded-xl border border-slate-700 bg-slate-900">
      <div className="border-b border-slate-700 px-6 py-4">
        <h2 className="text-xl font-semibold text-white">
          Recent Jobs
        </h2>
      </div>

      <table className="w-full">
        <thead className="bg-slate-800 text-left text-sm text-slate-300">
          <tr>
            <th className="px-6 py-3">Job</th>
            <th>Status</th>
            <th>Node</th>
          </tr>
        </thead>

        <tbody>
          {jobs.length === 0 ? (
            <tr>
              <td
                colSpan={3}
                className="px-6 py-10 text-center text-slate-400"
              >
                No jobs have been submitted.
              </td>
            </tr>
          ) : (
            jobs.map((job) => (
              <tr
                key={job.id}
                className="border-t border-slate-800"
              >
                <td className="px-6 py-4 text-white">
                  {job.name}
                </td>

                <td>
                  <span
                    className={`rounded px-2 py-1 text-sm ${badgeStyles[job.status]}`}
                  >
                    {job.status}
                  </span>
                </td>

                <td>{job.node}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </section>
  );
}
