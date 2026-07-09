import { Bell, Search } from "lucide-react";

export function Header() {
  return (
    <header className="header">
      <div>
        <h1>Dashboard</h1>

        <p>Monitor your NeuroMesh cluster in real time.</p>
      </div>

      <div className="header__actions">
        <div className="header__search">
          <Search size={18} />

          <input
            placeholder="Search nodes, jobs..."
            type="text"
          />
        </div>

        <button className="header__icon-button">
          <Bell size={18} />
        </button>

        <div className="header__user">
          <div className="header__avatar">
            A
          </div>

          <div>
            <strong>Admin</strong>

            <span>Online</span>
          </div>
        </div>
      </div>
    </header>
  );
}