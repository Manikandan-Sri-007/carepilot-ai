import { useState } from "react";

import AppLayout from "../components/layout/AppLayout";
import api from "../services/api";

export default function ReportAnalysisPage() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setError("");
    setResult(null);
    try {
      const formData = new FormData();
      formData.append("file", file);
      const { data } = await api.post("/analysis/report", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to analyze report");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppLayout>
      <div className="mx-auto max-w-4xl space-y-4">
        <div className="rounded-2xl border border-slate-200 bg-white/80 p-5 dark:border-slate-800 dark:bg-slate-900/70">
          <h1 className="text-2xl font-semibold">Medical Report Analyzer</h1>
          <p className="mt-1 text-sm text-slate-500">Upload PDF or image reports. OCR and summarization are supported by backend architecture.</p>
          <label className="mt-4 flex cursor-pointer items-center justify-center rounded-xl border border-dashed border-slate-400 p-6 text-sm hover:bg-slate-50 dark:hover:bg-slate-800">
            <input type="file" className="hidden" accept="application/pdf,image/*" onChange={handleUpload} />
            {loading ? "Analyzing report..." : "Click to upload PDF/Image"}
          </label>
        </div>

        {error && <div className="rounded-xl bg-red-50 p-3 text-red-700">{error}</div>}

        {result && (
          <div className="rounded-2xl border border-slate-200 bg-white/80 p-5 dark:border-slate-800 dark:bg-slate-900/70">
            <h2 className="text-xl font-semibold">Report Insights</h2>
            <p className="mt-3"><span className="font-semibold">Summary:</span> {result.summary}</p>
            <p className="mt-2"><span className="font-semibold">Abnormal Findings:</span> {result.abnormal_findings}</p>
            <p className="mt-2"><span className="font-semibold">Risk Level:</span> {result.risk_level}</p>
            <div className="mt-3">
              <p className="font-semibold">Discussion Points</p>
              <ul className="mt-2 list-disc space-y-1 pl-5 text-sm">
                {(result.discussion_points || []).map((point) => <li key={point}>{point}</li>)}
              </ul>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
