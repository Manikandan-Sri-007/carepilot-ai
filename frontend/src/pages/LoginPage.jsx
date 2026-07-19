import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";
import { getApiErrorMessage } from "../services/api";

export default function LoginPage() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm();
  const { login } = useAuth();
  const navigate = useNavigate();
  const [authError, setAuthError] = useState("");

  const onSubmit = async (values) => {
    setAuthError("");
    try {
      await login(values.email, values.password);
      navigate("/dashboard");
    } catch (error) {
      setAuthError(getApiErrorMessage(error, "Unable to sign in right now."));
    }
  };

  return (
    <div className="grid min-h-screen place-items-center bg-slate-100 p-4 dark:bg-slate-950">
      <form onSubmit={handleSubmit(onSubmit)} className="w-full max-w-md rounded-3xl border border-slate-200 bg-white p-6 shadow-xl dark:border-slate-800 dark:bg-slate-900">
        <h1 className="text-2xl font-semibold">Sign in to CarePilot AI</h1>
        <p className="mt-1 text-sm text-slate-500">Secure access to your health workspace.</p>

        <div className="mt-5 space-y-4">
          <input className="w-full rounded-xl border border-slate-300 px-3 py-2.5 dark:border-slate-700 dark:bg-slate-800" placeholder="Email" {...register("email", { required: true })} />
          {errors.email && <p className="text-xs text-red-600">Email is required</p>}
          <input type="password" className="w-full rounded-xl border border-slate-300 px-3 py-2.5 dark:border-slate-700 dark:bg-slate-800" placeholder="Password" {...register("password", { required: true })} />
          {errors.password && <p className="text-xs text-red-600">Password is required</p>}
          {authError && <p className="text-sm text-red-600">{authError}</p>}
        </div>

        <button disabled={isSubmitting} className="mt-5 w-full rounded-xl bg-teal-600 px-4 py-2.5 font-semibold text-white hover:bg-teal-700 disabled:opacity-60">
          {isSubmitting ? "Signing in..." : "Sign In"}
        </button>

        <div className="mt-4 flex justify-between text-sm">
          <Link to="/forgot-password" className="text-teal-600">Forgot password?</Link>
          <Link to="/register" className="text-slate-600 dark:text-slate-300">Create account</Link>
        </div>
      </form>
    </div>
  );
}
