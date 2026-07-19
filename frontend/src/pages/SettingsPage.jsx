import AppLayout from "../components/layout/AppLayout";

export default function SettingsPage() {
  return (
    <AppLayout>
      <div className="mx-auto max-w-3xl rounded-2xl border border-slate-200 bg-white/80 p-5 dark:border-slate-800 dark:bg-slate-900/70">
        <h1 className="text-2xl font-semibold">Settings</h1>
        <p className="mt-2 text-sm text-slate-500">
          Environment-specific options such as notification preferences, privacy controls, and integration keys can be extended here.
        </p>
      </div>
    </AppLayout>
  );
}
