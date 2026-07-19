import { HeartPulse, ShieldCheck, Sparkles } from "lucide-react";
import { Link } from "react-router-dom";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[linear-gradient(135deg,#f0fdfa_0%,#ecfdf5_35%,#eff6ff_100%)] p-6 dark:bg-[linear-gradient(135deg,#022c22_0%,#0f172a_40%,#111827_100%)]">
      <div className="mx-auto max-w-6xl rounded-[28px] border border-white/70 bg-white/70 p-8 shadow-2xl backdrop-blur-xl dark:border-slate-700 dark:bg-slate-900/70">
        <p className="text-sm uppercase tracking-[0.25em] text-teal-600">CarePilot AI</p>
        <h1 className="mt-2 max-w-3xl text-4xl font-semibold leading-tight text-slate-900 dark:text-white sm:text-5xl">
          Production-grade healthcare AI companion for symptom intelligence and report understanding.
        </h1>
        <p className="mt-4 max-w-2xl text-slate-600 dark:text-slate-300">
          Analyze symptoms, extract report insights, monitor risk levels, and guide patient communication with clinician-ready outputs.
        </p>

        <div className="mt-8 flex flex-wrap gap-3">
          <Link to="/register" className="rounded-xl bg-teal-600 px-5 py-3 font-semibold text-white hover:bg-teal-700">Get Started</Link>
          <Link to="/login" className="rounded-xl border border-slate-300 px-5 py-3 font-semibold text-slate-700 hover:bg-white dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-800">Sign In</Link>
        </div>

        <div className="mt-10 grid gap-4 sm:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white/70 p-4 dark:border-slate-700 dark:bg-slate-800/70"><HeartPulse className="text-teal-600" /><h3 className="mt-3 font-semibold">Symptom Intelligence</h3></div>
          <div className="rounded-2xl border border-slate-200 bg-white/70 p-4 dark:border-slate-700 dark:bg-slate-800/70"><ShieldCheck className="text-teal-600" /><h3 className="mt-3 font-semibold">Secure SaaS Architecture</h3></div>
          <div className="rounded-2xl border border-slate-200 bg-white/70 p-4 dark:border-slate-700 dark:bg-slate-800/70"><Sparkles className="text-teal-600" /><h3 className="mt-3 font-semibold">AI Assistant Ready for LLM</h3></div>
        </div>
      </div>
    </div>
  );
}
