export function Sidebar() {
  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900 p-6">
      <nav className="space-y-3">

        <div className="text-slate-100 font-medium">
          Dashboard
        </div>

        <div className="text-slate-400">
          Nodes
        </div>

        <div className="text-slate-400">
          Jobs
        </div>

      </nav>
    </aside>
  );
}