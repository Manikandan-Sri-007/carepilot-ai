import { useEffect, useMemo, useState } from "react";

import AppLayout from "../components/layout/AppLayout";
import api from "../services/api";
import { badgeColor, formatDate } from "../utils/format";

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [reports, setReports] = useState([]);
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        setError("");
        const [historyRes, reportsRes] = await Promise.all([api.get("/analysis/history"), api.get("/reports")]);
        setHistory(historyRes.data || []);
        setReports(reportsRes.data || []);
      } catch (err) {
        setHistory([]);
        setReports([]);
        setError(err?.response?.data?.detail || "Unable to load your health history right now.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const records = useMemo(() => {
    const symptomRows = history.map((item) => ({ ...item, record_type: "symptom", text: item.symptoms }));
    const reportRows = reports.map((item) => ({ ...item, record_type: "report", text: item.summary }));

    return [...symptomRows, ...reportRows]
      .filter((row) => filter === "all" || row.record_type === filter)
      .filter((row) => (row.text || "").toLowerCase().includes(query.toLowerCase()))
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }, [history, reports, filter, query]);

  return (
    <AppLayout>
      <div className="space-y-4">
        <div className="rounded-2xl border border-slate-200 bg-white/80 p-4 dark:border-slate-800 dark:bg-slate-900/70">
          <h1 className="text-2xl font-semibold">Health History</h1>
          <div className="mt-3 flex flex-col gap-2 sm:flex-row">
            <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search history" className="w-full rounded-xl border border-slate-300 px-3 py-2 dark:border-slate-700 dark:bg-slate-800" />
            <select value={filter} onChange={(e) => setFilter(e.target.value)} className="rounded-xl border border-slate-300 px-3 py-2 dark:border-slate-700 dark:bg-slate-800">
              <option value="all">All</option>
              <option value="symptom">Symptom Checks</option>
              <option value="report">Reports</option>
            </select>
          </div>
        </div>

        {loading && <div className="rounded-xl border border-slate-200 bg-white/80 p-4 text-sm text-slate-600 dark:border-slate-800 dark:bg-slate-900/70">Loading your records…</div>}
        {error && <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}

        {!loading && !error && records.length === 0 && (
          <div className="rounded-xl border border-slate-200 bg-white/80 p-4 text-sm text-slate-600 dark:border-slate-800 dark:bg-slate-900/70">
            No history entries yet. Complete a symptom check or upload a report to start building your timeline.
          </div>
        )}

        <div className="space-y-2">
          {records.map((row) => (
            <div key={`${row.record_type}-${row.id}`} className="rounded-xl border border-slate-200 bg-white/80 p-4 dark:border-slate-800 dark:bg-slate-900/70">
              <div className="flex items-center justify-between gap-2">
                <span className="rounded-full bg-slate-100 px-2 py-1 text-xs uppercase dark:bg-slate-800">{row.record_type}</span>
                <span className="text-xs text-slate-500">{formatDate(row.created_at)}</span>
              </div>
              <p className="mt-2 text-sm text-slate-700 dark:text-slate-200">{row.text || "No details recorded yet."}</p>
              {row.risk_level && <span className={`mt-2 inline-flex rounded-full px-2 py-1 text-xs font-semibold ${badgeColor(row.risk_level)}`}>{row.risk_level}</span>}
            </div>
          ))}
        </div>
      </div>
    </AppLayout>
  );
}
