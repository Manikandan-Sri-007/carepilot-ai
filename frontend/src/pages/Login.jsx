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
            await api.post("/login", {
                email: normalizedEmail,
                password
            });

            // The JWT is held in the server-issued HttpOnly cookie. Verify it by
            // loading the authoritative profile before entering the application.
            await api.get("/profile");
            sessionStorage.setItem("carepilot_authenticated", "true");

            navigate("/dashboard");
        } catch (error) {
            alert("Invalid email or password");
            console.error(error);
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
