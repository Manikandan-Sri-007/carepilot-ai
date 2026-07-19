import { Bell, Moon, Sun, UserCircle2 } from "lucide-react";
import { Link } from "react-router-dom";

import { useAuth } from "../../hooks/useAuth";
import { useTheme } from "../../hooks/useTheme";

export default function TopNav() {
  const { logout, user } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="sticky top-0 z-20 flex items-center justify-between border-b border-slate-200 bg-white/75 px-4 py-3 backdrop-blur-xl dark:border-slate-800 dark:bg-slate-950/70 sm:px-6">
      <div>
        <p className="text-xs uppercase tracking-[0.2em] text-teal-600">Healthcare AI</p>
        <h2 className="text-lg font-semibold text-slate-900 dark:text-white">Welcome back, {user?.name || "Member"}</h2>
      </div>

      <div className="flex items-center gap-2">
        <button onClick={toggleTheme} className="rounded-xl border border-slate-200 p-2 text-slate-600 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800" aria-label="Toggle theme">
          {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
        </button>
        <button className="rounded-xl border border-slate-200 p-2 text-slate-600 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800" aria-label="Notifications">
          <Bell size={18} />
        </button>
        <Link to="/profile" className="inline-flex items-center gap-2 rounded-xl border border-slate-200 px-3 py-2 text-sm text-slate-700 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800">
          <UserCircle2 size={18} />
          Profile
        </Link>
        <button onClick={logout} className="rounded-xl bg-slate-900 px-3 py-2 text-sm font-medium text-white hover:bg-slate-800 dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-white">
          Logout
        </button>
      </div>
    </header>
  );
}
