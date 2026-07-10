import type { ReactNode } from "react";

import { Header } from "./Header";
import { Sidebar } from "./Sidebar";

interface ShellProps {
  children: ReactNode;
}

export function Shell({
  children,
}: ShellProps) {
  return (
    <div className="min-h-screen bg-slate-950">

      <Header />

      <div className="flex">

        <Sidebar />

        <main className="flex-1 p-8">
          {children}
        </main>

      </div>

    </div>
  );
}