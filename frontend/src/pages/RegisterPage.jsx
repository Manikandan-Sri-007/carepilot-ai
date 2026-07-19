import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

export default function RegisterPage() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm();
  const { register: registerUser } = useAuth();
  const navigate = useNavigate();

  const onSubmit = async (values) => {
    await registerUser(values);
    navigate("/dashboard");
  };

  return (
    <div className="grid min-h-screen place-items-center bg-slate-100 p-4 dark:bg-slate-950">
      <form onSubmit={handleSubmit(onSubmit)} className="w-full max-w-md rounded-3xl border border-slate-200 bg-white p-6 shadow-xl dark:border-slate-800 dark:bg-slate-900">
        <h1 className="text-2xl font-semibold">Create your account</h1>

        <div className="mt-5 space-y-3">
          <input className="w-full rounded-xl border border-slate-300 px-3 py-2.5 dark:border-slate-700 dark:bg-slate-800" placeholder="Name" {...register("name", { required: true })} />
          <input className="w-full rounded-xl border border-slate-300 px-3 py-2.5 dark:border-slate-700 dark:bg-slate-800" placeholder="Email" {...register("email", { required: true })} />
          <input type="password" className="w-full rounded-xl border border-slate-300 px-3 py-2.5 dark:border-slate-700 dark:bg-slate-800" placeholder="Password" {...register("password", { required: true, minLength: 8 })} />
          <input type="number" className="w-full rounded-xl border border-slate-300 px-3 py-2.5 dark:border-slate-700 dark:bg-slate-800" placeholder="Age" {...register("age", { valueAsNumber: true })} />
          <select className="w-full rounded-xl border border-slate-300 px-3 py-2.5 dark:border-slate-700 dark:bg-slate-800" {...register("gender")}>
            <option value="">Select gender</option>
            <option value="Female">Female</option>
            <option value="Male">Male</option>
            <option value="Other">Other</option>
          </select>
          {errors.password && <p className="text-xs text-red-600">Password must be at least 8 characters.</p>}
        </div>

        <button disabled={isSubmitting} className="mt-5 w-full rounded-xl bg-teal-600 px-4 py-2.5 font-semibold text-white hover:bg-teal-700 disabled:opacity-60">
          {isSubmitting ? "Creating account..." : "Create account"}
        </button>

        <p className="mt-4 text-sm text-slate-600 dark:text-slate-300">Already have an account? <Link className="text-teal-600" to="/login">Sign in</Link></p>
      </form>
    </div>
  );
}
