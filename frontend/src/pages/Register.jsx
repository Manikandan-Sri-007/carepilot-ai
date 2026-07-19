import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import api from "../services/api";

function Register() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleRegister = async (event) => {
        event.preventDefault();
        const normalizedName = name.trim();
        const normalizedEmail = email.trim().toLowerCase();

        if (normalizedName.length < 2) {
            alert("Please enter your full name.");
            return;
        }

        if (password.length < 8) {
            alert("Password must be at least 8 characters.");
            return;
        }

        setLoading(true);

        try {
            await api.post("/auth/register", {
                name: normalizedName,
                email: normalizedEmail,
                password
            });

            alert("Registration successful. Please log in.");
            navigate("/login");
        } catch (error) {
            const message = error.response?.data?.detail
                || (error.request ? "CarePilot AI is temporarily unavailable. Please try again shortly." : "Unable to create account");
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
                    <h1 className="auth-title">Create your secure care workspace</h1>
                    <p className="auth-description">
                        Get started with a calm, professional experience for symptom guidance, report review, and ongoing support.
                    </p>
                    <div className="auth-highlights">
                        <span>Secure account</span>
                        <span>Private history</span>
                    </div>
                </div>

                <form onSubmit={handleRegister} className="auth-form">
                    <div>
                        <h2 className="text-2xl font-semibold text-slate-900">Create account</h2>
                        <p className="auth-subtitle">Begin your personalized care experience.</p>
                    </div>

                    <label className="form-label" htmlFor="name">Full name</label>
                    <input
                        id="name"
                        type="text"
                        className="form-control"
                        placeholder="Enter your name"
                        value={name}
                        onChange={(event) => setName(event.target.value)}
                        required
                    />

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
                        placeholder="Choose a password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                        required
                    />

                    <button className="btn-primary w-full" type="submit" disabled={loading}>
                        {loading ? "Creating account..." : "Register"}
                    </button>

                    <p className="auth-link">
                        Already have an account? <Link to="/login" className="font-semibold text-brand-600">Login</Link>
                    </p>
                </form>
            </div>
        </div>
    );
}

export default Register;
