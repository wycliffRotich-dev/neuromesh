import { DashboardPage } from "./dashboard/DashboardPage";
import { Shell } from "./components/layout/Shell";

export default function App() {
  return (
    <Shell>
      <DashboardPage />
    </Shell>
  );
}