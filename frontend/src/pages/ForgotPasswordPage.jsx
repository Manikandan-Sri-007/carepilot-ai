import { useState } from "react";
import { useForm } from "react-hook-form";

import api from "../services/api";

export default function ForgotPasswordPage() {
  const [message, setMessage] = useState("");
  const { register, handleSubmit, formState: { isSubmitting } } = useForm();

  const onSubmit = async (values) => {
    const { data } = await api.post("/auth/forgot-password", values);
    setMessage(data.message || "Request submitted");
  };

  return (
    <div className="grid min-h-screen place-items-center bg-slate-100 p-4 dark:bg-slate-950">
      <form onSubmit={handleSubmit(onSubmit)} className="w-full max-w-md rounded-3xl border border-slate-200 bg-white p-6 shadow-xl dark:border-slate-800 dark:bg-slate-900">
        <h1 className="text-2xl font-semibold">Forgot password</h1>
        <p className="mt-1 text-sm text-slate-500">Enter your account email to generate a reset flow token.</p>
        <input className="mt-4 w-full rounded-xl border border-slate-300 px-3 py-2.5 dark:border-slate-700 dark:bg-slate-800" placeholder="Email" {...register("email", { required: true })} />
        <button disabled={isSubmitting} className="mt-4 w-full rounded-xl bg-teal-600 px-4 py-2.5 font-semibold text-white hover:bg-teal-700 disabled:opacity-60">
          {isSubmitting ? "Submitting..." : "Send reset request"}
        </button>
        {message && <p className="mt-3 text-sm text-emerald-600">{message}</p>}
      </form>
    </div>
  );
}
