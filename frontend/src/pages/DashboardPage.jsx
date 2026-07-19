import { useEffect, useMemo, useState } from "react";

import { HealthScoreChart, SymptomTrendChart } from "../components/charts/HealthCharts";
import AppLayout from "../components/layout/AppLayout";
import StatCard from "../components/ui/StatCard";
import { useAuth } from "../hooks/useAuth";
import api from "../services/api";

export default function DashboardPage() {
  const [history, setHistory] = useState([]);
  const [reports, setReports] = useState([]);
  const { user } = useAuth();

  useEffect(() => {
    async function load() {
      try {
        const [historyRes, reportsRes] = await Promise.all([
          api.get("/analysis/history"),
          api.get("/reports"),
        ]);
        setHistory(historyRes.data || []);
        setReports(reportsRes.data || []);
      } catch (error) {
        setHistory([]);
        setReports([]);
      }
    }
    load();
  }, []);

  const score = useMemo(() => {
    if (!history.length) return 80;
    const avgRisk = history.reduce((acc, item) => {
      if (item.risk_level === "High") return acc + 30;
      if (item.risk_level === "Medium") return acc + 15;
      return acc + 5;
    }, 0) / history.length;
    return Math.max(30, 100 - Math.round(avgRisk));
  }, [history]);

  const chartData = useMemo(() => history.slice(0, 7).reverse().map((row, index) => ({
    date: `${index + 1}`,
    score: row.risk_level === "High" ? 45 : row.risk_level === "Medium" ? 65 : 85,
    checks: index + 1,
  })), [history]);

  const stats = [
    { title: "Health Score", value: `${score}/100`, subtitle: "Dynamic risk-weighted index" },
    { title: "Recent Analysis", value: history.length, subtitle: "Symptom checks recorded" },
    { title: "Risk Level", value: history[0]?.risk_level || "Low", subtitle: "Latest AI assessment" },
    { title: "Total Reports", value: reports.length, subtitle: "Medical files analyzed" },
    { title: "Upcoming Reminders", value: 2, subtitle: "Medication and follow-up" },
  ];

  return (
    <AppLayout>
      <section className="space-y-4">
        <div className="rounded-3xl border border-teal-100 bg-gradient-to-r from-teal-600 to-cyan-600 p-6 text-white shadow-xl">
          <p className="text-xs uppercase tracking-[0.22em]">Patient Dashboard</p>
          <h1 className="mt-2 text-3xl font-semibold">{user?.name || "Patient"}, your care intelligence hub is live.</h1>
          <p className="mt-2 text-white/90">This AI does not replace professional medical advice.</p>
        </div>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
          {stats.map((item) => <StatCard key={item.title} {...item} />)}
        </div>

        <div className="grid gap-4 xl:grid-cols-2">
          <HealthScoreChart data={chartData} />
          <SymptomTrendChart data={chartData} />
        </div>
      </section>
    </AppLayout>
  );
}
