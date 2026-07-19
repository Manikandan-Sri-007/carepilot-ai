import SideNav from "./SideNav";
import TopNav from "./TopNav";

export default function AppLayout({ children }) {
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_10%_0%,_rgba(20,184,166,0.15),_transparent_30%),linear-gradient(120deg,#f7fafc_0%,#eef7ff_45%,#f8fafc_100%)] text-slate-900 dark:bg-[radial-gradient(circle_at_10%_0%,_rgba(20,184,166,0.16),_transparent_35%),linear-gradient(120deg,#020617_0%,#0f172a_45%,#111827_100%)] dark:text-slate-100">
      <div className="flex min-h-screen">
        <SideNav />
        <main className="w-full">
          <TopNav />
          <div className="p-4 sm:p-6">{children}</div>
        </main>
      </div>
    </div>
  );
}
