import { useEffect, useState } from "react";

import AppLayout from "../components/layout/AppLayout";
import StatCard from "../components/ui/StatCard";
import api from "../services/api";

export default function AdminDashboardPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const response = await api.get("/admin/dashboard");
        setData(response.data);
      } catch {
        setData({
          user_count: 0,
          active_users: 0,
          reports_processed: 0,
          symptom_checks: 0,
          chats_answered: 0,
        });
      }
    }
    load();
  }, []);

  return (
    <AppLayout>
      <div className="space-y-4">
        <h1 className="text-2xl font-semibold">Admin Dashboard</h1>
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
          <StatCard title="User Count" value={data?.user_count ?? "-"} subtitle="Total registered" />
          <StatCard title="Active Users" value={data?.active_users ?? "-"} subtitle="Enabled accounts" />
          <StatCard title="Reports Processed" value={data?.reports_processed ?? "-"} subtitle="Documents analyzed" />
          <StatCard title="Symptom Checks" value={data?.symptom_checks ?? "-"} subtitle="AI triage events" />
          <StatCard title="Chats Answered" value={data?.chats_answered ?? "-"} subtitle="Assistant interactions" />
        </div>
      </div>
    </AppLayout>
  );
}
