import {
  Activity,
  Box,
  Cpu,
  LayoutDashboard,
  Settings,
} from "lucide-react";

const items = [
  {
    label: "Dashboard",
    icon: LayoutDashboard,
    active: true,
  },
  {
    label: "Nodes",
    icon: Cpu,
    active: false,
  },
  {
    label: "Jobs",
    icon: Box,
    active: false,
  },
  {
    label: "Metrics",
    icon: Activity,
    active: false,
  },
  {
    label: "Settings",
    icon: Settings,
    active: false,
  },
];

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar__logo">
        <div className="sidebar__logo-mark">N</div>

        <div>
          <h2>NeuroMesh</h2>
          <span>Control Plane</span>
        </div>
      </div>

      <nav className="sidebar__nav">
        {items.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.label}
              className={`sidebar__item ${
                item.active ? "sidebar__item--active" : ""
              }`}
            >
              <Icon size={18} />

              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="sidebar__footer">
        v0.1.0
      </div>
    </aside>
  );
}