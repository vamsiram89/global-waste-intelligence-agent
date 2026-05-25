import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Inventory from "./pages/Inventory";
import WastePrediction from "./pages/WastePrediction";
import ActionRecommendations from "./pages/ActionRecommendations";
import NgoMatching from "./pages/NgoMatching";
import Analytics from "./pages/Analytics";
import Settings from "./pages/Settings";

function AppShell() {
  const location = useLocation();
  const isLogin = location.pathname === "/login";

  if (isLogin) {
    return <Login />;
  }

  return (
    <div className="min-h-screen bg-paper">
      <Sidebar />
      <div className="xl:pl-72">
        <Topbar />
        <main className="px-4 py-6 lg:px-8">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/inventory" element={<Inventory />} />
            <Route path="/prediction" element={<WastePrediction />} />
            <Route path="/actions" element={<ActionRecommendations />} />
            <Route path="/ngos" element={<NgoMatching />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/*" element={<AppShell />} />
    </Routes>
  );
}
