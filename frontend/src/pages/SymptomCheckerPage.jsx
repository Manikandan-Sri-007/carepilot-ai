import { useState } from "react";
import { useForm } from "react-hook-form";

import AppLayout from "../components/layout/AppLayout";
import { badgeColor } from "../utils/format";
import api from "../services/api";

export default function SymptomCheckerPage() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const { register, handleSubmit, formState: { isSubmitting } } = useForm();

  const onSubmit = async (values) => {
    setError("");
    setResult(null);
    try {
      const { data } = await api.post("/analysis/symptoms", values);
      setResult(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to analyze symptoms right now.");
    }
  };

  return (
    <AppLayout>
      <div className="mx-auto max-w-4xl space-y-4">
        <div className="rounded-2xl border border-slate-200 bg-white/80 p-5 dark:border-slate-800 dark:bg-slate-900/70">
          <h1 className="text-2xl font-semibold">AI Symptom Analyzer</h1>
          <p className="mt-1 text-sm text-slate-500">Enter symptoms like fever, headache, cough to estimate possible conditions and risk.</p>
          <p className="mt-2 rounded-xl bg-amber-50 p-2 text-sm text-amber-700">This AI does not replace professional medical advice.</p>

          <form onSubmit={handleSubmit(onSubmit)} className="mt-4 space-y-3">
            <textarea className="h-32 w-full rounded-xl border border-slate-300 p-3 dark:border-slate-700 dark:bg-slate-800" placeholder="fever, headache, cough" {...register("symptoms", { required: true })} />
            <button disabled={isSubmitting} className="rounded-xl bg-teal-600 px-4 py-2.5 font-semibold text-white hover:bg-teal-700 disabled:opacity-60">
              {isSubmitting ? "Analyzing..." : "Analyze Symptoms"}
            </button>
          </form>
        </div>

        {error && <div className="rounded-xl bg-red-50 p-3 text-red-700">{error}</div>}

        {result && (
          <div className="rounded-2xl border border-slate-200 bg-white/80 p-5 dark:border-slate-800 dark:bg-slate-900/70">
            <h2 className="text-xl font-semibold">Analysis Result</h2>
            <div className="mt-3 grid gap-3 sm:grid-cols-2">
              <div><p className="text-sm text-slate-500">Condition</p><p className="font-semibold">{result.condition}</p></div>
              <div><p className="text-sm text-slate-500">Probability</p><p className="font-semibold">{Math.round(result.probability * 100)}%</p></div>
              <div><p className="text-sm text-slate-500">Risk</p><span className={`rounded-full px-3 py-1 text-sm font-semibold ${badgeColor(result.risk_level)}`}>{result.risk_level}</span></div>
              <div><p className="text-sm text-slate-500">Recommendation</p><p className="font-medium">{result.recommendation}</p></div>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
