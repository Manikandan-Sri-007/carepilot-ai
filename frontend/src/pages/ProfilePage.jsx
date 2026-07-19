import { useEffect } from "react";
import { useForm } from "react-hook-form";

import AppLayout from "../components/layout/AppLayout";
import { useAuth } from "../hooks/useAuth";
import api from "../services/api";

export default function ProfilePage() {
  const { user, refreshProfile } = useAuth();
  const { register, handleSubmit, reset, formState: { isSubmitting } } = useForm();

  useEffect(() => {
    if (user) reset(user);
  }, [user, reset]);

  const onSubmit = async (values) => {
    await api.put("/users/profile", values);
    await refreshProfile();
  };

  return (
    <AppLayout>
      <form onSubmit={handleSubmit(onSubmit)} className="mx-auto max-w-3xl rounded-2xl border border-slate-200 bg-white/80 p-5 dark:border-slate-800 dark:bg-slate-900/70">
        <h1 className="text-2xl font-semibold">Profile Management</h1>
        <p className="mt-1 text-sm text-slate-500">Update personal and health preference information.</p>

        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <input className="rounded-xl border border-slate-300 px-3 py-2 dark:border-slate-700 dark:bg-slate-800" placeholder="Name" {...register("name")} />
          <input type="number" className="rounded-xl border border-slate-300 px-3 py-2 dark:border-slate-700 dark:bg-slate-800" placeholder="Age" {...register("age", { valueAsNumber: true })} />
          <input className="rounded-xl border border-slate-300 px-3 py-2 dark:border-slate-700 dark:bg-slate-800" placeholder="Gender" {...register("gender")} />
          <input className="rounded-xl border border-slate-300 px-3 py-2 dark:border-slate-700 dark:bg-slate-800" placeholder="Phone" {...register("phone")} />
          <textarea className="sm:col-span-2 rounded-xl border border-slate-300 px-3 py-2 dark:border-slate-700 dark:bg-slate-800" placeholder="Health goals" {...register("health_goals")} />
        </div>

        <button disabled={isSubmitting} className="mt-4 rounded-xl bg-teal-600 px-4 py-2.5 font-semibold text-white hover:bg-teal-700 disabled:opacity-60">Save Profile</button>
      </form>
    </AppLayout>
  );
}
