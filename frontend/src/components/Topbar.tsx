import { Bell, CalendarDays, Menu, Search } from "lucide-react";
import { NavLink } from "react-router-dom";

const mobileNav = [
  ["Dashboard", "/dashboard"],
  ["Inventory", "/inventory"],
  ["Prediction", "/prediction"],
  ["Actions", "/actions"],
  ["NGOs", "/ngos"],
  ["Analytics", "/analytics"],
  ["Settings", "/settings"],
];

export default function Topbar() {
  const today = new Intl.DateTimeFormat("en", { month: "short", day: "numeric", year: "numeric" }).format(new Date());

  return (
    <header className="sticky top-0 z-20 border-b border-slate-200 bg-paper/88 px-4 py-4 backdrop-blur lg:px-8">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex items-center gap-3">
          <button className="grid h-10 w-10 place-items-center rounded-xl bg-white text-navy shadow-sm xl:hidden" aria-label="Open menu">
            <Menu className="h-5 w-5" />
          </button>
          <div className="relative w-full min-w-0 sm:w-96">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input className="h-11 w-full rounded-2xl border border-slate-200 bg-white pl-10 pr-4 text-sm outline-none transition focus:border-sky focus:ring-4 focus:ring-blue-100" placeholder="Search inventory, partners, alerts..." />
          </div>
        </div>
        <div className="flex items-center justify-between gap-3 lg:justify-end">
          <div className="hidden items-center gap-2 rounded-2xl bg-white px-4 py-2 text-sm font-semibold text-slate-600 shadow-sm sm:flex">
            <CalendarDays className="h-4 w-4 text-sky" />
            {today}
          </div>
          <button className="relative grid h-11 w-11 place-items-center rounded-2xl bg-white text-slate-600 shadow-sm" aria-label="Notifications">
            <Bell className="h-5 w-5" />
            <span className="absolute right-3 top-3 h-2 w-2 rounded-full bg-danger" />
          </button>
          <div className="flex items-center gap-3 rounded-2xl bg-white px-3 py-2 shadow-sm">
            <div className="grid h-8 w-8 place-items-center rounded-full bg-navy text-xs font-bold text-white">U</div>
            <div className="hidden sm:block">
              <p className="text-sm font-bold text-ink">User</p>
              <p className="text-xs text-slate-500">Operations Lead</p>
            </div>
          </div>
        </div>
      </div>
      <div className="mt-3 flex gap-2 overflow-x-auto pb-1 xl:hidden">
        {mobileNav.map(([label, to]) => (
          <NavLink key={to} to={to} className={({ isActive }) => `whitespace-nowrap rounded-full px-3 py-1.5 text-xs font-semibold ${isActive ? "bg-navy text-white" : "bg-white text-slate-600"}`}>
            {label}
          </NavLink>
        ))}
      </div>
    </header>
  );
}
