import { NavLink } from "react-router-dom";
import { BarChart3, ClipboardCheck, Gauge, HeartHandshake, LayoutDashboard, Package, Settings, Sparkles, ExternalLink } from "lucide-react";

const navItems = [
  { label: "Dashboard", to: "/dashboard", icon: LayoutDashboard },
  { label: "Inventory", to: "/inventory", icon: Package },
  { label: "Waste Prediction", to: "/prediction", icon: Gauge },
  { label: "Action Recommendations", to: "/actions", icon: ClipboardCheck },
  { label: "NGO Matching", to: "/ngos", icon: HeartHandshake },
  { label: "Analytics", to: "/analytics", icon: BarChart3 },
  { label: "Settings", to: "/settings", icon: Settings },
];

export default function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 z-30 hidden w-72 border-r border-slate-200 bg-white/92 px-4 py-5 backdrop-blur xl:block">
      <div className="flex items-center gap-3 rounded-2xl bg-navy px-4 py-3 text-white shadow-soft">
        <div className="grid h-10 w-10 place-items-center rounded-xl bg-white/15">
          <Sparkles className="h-5 w-5 text-mint" />
        </div>
        <div>
          <p className="text-sm font-bold">Smart Food Safe</p>
          <p className="text-xs text-blue-100">Waste Intelligence</p>
        </div>
      </div>

      <nav className="mt-8 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-semibold transition ${
                isActive ? "bg-blue-50 text-navy shadow-sm" : "text-slate-600 hover:bg-slate-50 hover:text-navy"
              }`
            }
          >
            <item.icon className="h-4 w-4" />
            {item.label}
          </NavLink>
        ))}
        <a className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-semibold text-slate-600 transition hover:bg-slate-50 hover:text-navy" href="http://localhost:8000/docs" target="_blank" rel="noreferrer">
          <ExternalLink className="h-4 w-4" />
          API Docs
        </a>
      </nav>

      <div className="absolute bottom-5 left-4 right-4 rounded-2xl bg-gradient-to-br from-mint to-blue-50 p-4">
        <p className="text-sm font-bold text-ink">Human approval built in</p>
        <p className="mt-2 text-xs leading-5 text-slate-600">Redistribution workflows stay pending until safety and partner checks are confirmed.</p>
      </div>
    </aside>
  );
}
