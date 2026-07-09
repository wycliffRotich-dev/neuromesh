import type { ReactNode } from "react";

import { Header } from "./Header";
import { Sidebar } from "./Sidebar";

type ShellProps = {
  children: ReactNode;
};

export function Shell({ children }: ShellProps) {
  return (
    <div className="shell">
      <Sidebar />

      <div className="shell__main">
        <Header />

        <main className="shell__content">
          {children}
        </main>
      </div>
    </div>
  );
}