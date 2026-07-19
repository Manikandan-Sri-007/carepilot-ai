import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import api from "../services/api";

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (event) => {
        event.preventDefault();
        const normalizedEmail = email.trim().toLowerCase();

        if (password.length < 8) {
            alert("Password must be at least 8 characters.");
            return;
        }

        setLoading(true);

        try {
            const response = await api.post("/auth/login", {
                email: normalizedEmail,
                password
            });

            const token = response.data?.access_token;
            if (!token) {
                throw new Error("The server did not return an authentication token.");
            }

            localStorage.setItem("carepilot_access_token", token);
            localStorage.setItem("carepilot_refresh_token", response.data?.refresh_token || "");
            localStorage.setItem("carepilot_authenticated", "true");

            navigate("/dashboard");
        } catch (error) {
            sessionStorage.removeItem("carepilot_access_token");
            const message = error.response?.data?.detail
                || (error.request ? "CarePilot AI is temporarily unavailable. Please try again shortly." : error.message)
                || "Unable to sign in. Please try again.";
            alert(message);
            if (import.meta.env.DEV) console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-card">
                <div className="auth-hero">
                    <div className="auth-badge">CarePilot AI</div>
                    <h1 className="auth-title">Your intelligent healthcare assistant</h1>
                    <p className="auth-description">
                        Secure access to symptom review, medical insights, and patient-focused care support.
                    </p>
                    <div className="auth-highlights">
                        <span>Protected access</span>
                        <span>Clinical-ready guidance</span>
                    </div>
                </div>

                <form onSubmit={handleLogin} className="auth-form">
                    <div>
                        <h2 className="text-2xl font-semibold text-slate-900">Welcome back</h2>
                        <p className="auth-subtitle">Sign in to continue your care journey.</p>
                    </div>

                    <label className="form-label" htmlFor="email">Email</label>
                    <input
                        id="email"
                        type="email"
                        className="form-control"
                        placeholder="you@example.com"
                        value={email}
                        onChange={(event) => setEmail(event.target.value)}
                        required
                    />

                    <label className="form-label" htmlFor="password">Password</label>
                    <input
                        id="password"
                        type="password"
                        className="form-control"
                        placeholder="Enter your password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                        required
                    />

                    <button className="btn-primary w-full" type="submit" disabled={loading}>
                        {loading ? "Signing in..." : "Login"}
                    </button>

                    <p className="auth-link">
                        New to CarePilot AI? <Link to="/register" className="font-semibold text-brand-600">Create an account</Link>
                    </p>
                </form>
            </div>
        </div>
    );
}

export default Login;
