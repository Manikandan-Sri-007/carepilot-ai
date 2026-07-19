import { Activity, Bot, FileText, Gauge, History, Settings, Shield, Stethoscope, UserCircle } from "lucide-react";
import { NavLink } from "react-router-dom";

const links = [
  { to: "/dashboard", label: "Dashboard", icon: Gauge },
  { to: "/symptom-checker", label: "Symptom Checker", icon: Stethoscope },
  { to: "/report-analysis", label: "Report Analysis", icon: FileText },
  { to: "/history", label: "Health History", icon: History },
  { to: "/assistant", label: "AI Assistant", icon: Bot },
  { to: "/profile", label: "Profile", icon: UserCircle },
  { to: "/admin", label: "Admin", icon: Shield },
  { to: "/settings", label: "Settings", icon: Settings },
];

export default function SideNav() {
  return (
    <aside className="hidden w-72 shrink-0 border-r border-slate-200 bg-white/70 p-5 backdrop-blur-xl lg:block dark:border-slate-800 dark:bg-slate-950/60">
      <div className="mb-8 flex items-center gap-3">
        <div className="rounded-2xl bg-teal-600 p-2 text-white shadow-lg shadow-teal-500/20">
          <Activity size={20} />
        </div>
        <div>
          <p className="text-xs uppercase tracking-[0.22em] text-slate-500 dark:text-slate-400">CarePilot</p>
          <h1 className="text-lg font-semibold text-slate-900 dark:text-white">AI Platform</h1>
        </div>
      </div>

      <nav className="space-y-1">
        {links.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) => `flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition ${
              isActive
                ? "bg-teal-600 text-white"
                : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
            }`}
          >
            <Icon size={16} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
