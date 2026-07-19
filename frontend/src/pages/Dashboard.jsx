import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import api from "../services/api";
import "./Dashboard.css";

const notProvided = (value) => value === null || value === undefined || value === "" ? "Not Provided" : value;

function Dashboard() {
    const navigate = useNavigate();
    const [dashboard, setDashboard] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [prompt, setPrompt] = useState("");
    const [assistantReply, setAssistantReply] = useState("");
    const [assistantLoading, setAssistantLoading] = useState(false);

    useEffect(() => {
        const loadDashboard = async () => {
            try {
                setLoading(true);
                setError("");
                const response = await api.get("/dashboard");
                setDashboard(response.data);
            } catch (err) {
                console.error(err);
                setError("We could not load your care dashboard. Please refresh and try again.");
            } finally {
                setLoading(false);
            }
        };
        loadDashboard();
    }, []);

    const handleAssistantPrompt = async (event) => {
        event.preventDefault();
        if (!prompt.trim()) return;

        try {
            setAssistantLoading(true);
            const response = await api.post("/assistant/chat", { message: prompt.trim() });
            setAssistantReply(response.data?.response || "No response is available right now.");
        } catch (err) {
            console.error(err);
            setAssistantReply("The assistant is temporarily unavailable. Please try again later.");
        } finally {
            setAssistantLoading(false);
        }
    };

    const profile = dashboard?.profile;
    const snapshot = dashboard?.health_snapshot;
    const activity = dashboard?.recent_activity;
    const profileIncomplete = !profile || [profile.age, profile.gender, profile.profile_details].some(
        (value) => value === null || value === undefined || value === ""
    );

    return (
        <div className="app-shell dashboard-shell">
            <Sidebar />
            <main className="app-main">
                <Navbar />
                <div className="content dashboard-content">
                    <section className="dashboard-hero">
                        <div>
                            <p className="eyebrow">CarePilot AI</p>
                            <h1>Patient dashboard</h1>
                            <p>Your private view of profile information, care activity, and next steps.</p>
                        </div>
                        {profileIncomplete && !loading && (
                            <button className="dashboard-action" onClick={() => navigate("/profile")}>Complete profile</button>
                        )}
                    </section>

                    {loading && <section className="dashboard-card dashboard-loading">Loading your care information…</section>}
                    {error && <section className="dashboard-card dashboard-error">{error}</section>}

                    {!loading && !error && (
                        <div className="dashboard-layout">
                            <div className="dashboard-primary">
                                <section className="dashboard-card">
                                    <div className="section-heading"><div><p className="eyebrow">Patient overview</p><h2>Profile information</h2></div></div>
                                    <div className="patient-grid">
                                        <Detail label="Name" value={notProvided(profile?.name)} />
                                        <Detail label="Email" value={notProvided(profile?.email)} />
                                        <Detail label="Age" value={notProvided(profile?.age)} />
                                        <Detail label="Gender" value={notProvided(profile?.gender)} />
                                        <Detail label="Patient ID" value={notProvided(profile?.id)} />
                                        <Detail label="Profile details" value={notProvided(profile?.profile_details)} />
                                    </div>
                                    {profileIncomplete && <button className="profile-notice" onClick={() => navigate("/profile")}>Some profile details are not provided. Complete your profile.</button>}
                                </section>

                                <section className="dashboard-card">
                                    <div className="section-heading"><div><p className="eyebrow">Appointment information</p><h2>Care scheduling</h2></div></div>
                                    <div className="empty-state">No appointments scheduled</div>
                                </section>

                                <section className="dashboard-card">
                                    <div className="section-heading"><div><p className="eyebrow">Health snapshot</p><h2>Latest recorded analysis</h2></div>{snapshot?.risk_level && <span className="risk-badge">{snapshot.risk_level}</span>}</div>
                                    <div className="snapshot-grid">
                                        <Detail label="Health problem" value={snapshot?.health_problem || "No recent health issue detected"} />
                                        <Detail label="Latest analysis" value={snapshot?.latest_analysis_type || "Not Available"} />
                                        <Detail label="Risk level" value={snapshot?.risk_level || "Not Available"} />
                                    </div>
                                </section>

                                <section className="dashboard-card">
                                    <p className="eyebrow">Recent AI activity</p>
                                    {activity ? <div className="activity-row"><div><strong>{activity.analysis_type}</strong><span>{activity.created_at ? new Date(activity.created_at).toLocaleString() : "Date not available"}</span></div><span className="activity-dot" /></div> : <div className="empty-state">No recent AI activity</div>}
                                </section>
                            </div>

                            <aside className="dashboard-secondary">
                                <section className="dashboard-card ask-card">
                                    <p className="eyebrow">Ask CarePilot AI</p><h2>How can we help?</h2>
                                    <p>Describe symptoms or ask a health question to receive guidance.</p>
                                    <form onSubmit={handleAssistantPrompt}>
                                        <textarea value={prompt} onChange={(event) => setPrompt(event.target.value)} placeholder="Describe your concern" aria-label="Your health question" />
                                        <button className="dashboard-action" type="submit" disabled={assistantLoading || !prompt.trim()}>{assistantLoading ? "Thinking…" : "Ask CarePilot AI"}</button>
                                    </form>
                                    {assistantReply && <div className="assistant-reply">{assistantReply}</div>}
                                </section>
                                <section className="dashboard-card"><p className="eyebrow">Quick actions</p><div className="quick-actions">
                                    <button onClick={() => navigate("/symptoms")}>Analyze symptoms <span>→</span></button>
                                    <button onClick={() => navigate("/reports")}>Upload medical report <span>→</span></button>
                                    <button onClick={() => navigate("/history")}>View history <span>→</span></button>
                                    <button onClick={() => navigate("/profile")}>Manage profile <span>→</span></button>
                                </div></section>
                            </aside>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}

function Detail({ label, value }) {
    return <div className="dashboard-detail"><span>{label}</span><strong>{value}</strong></div>;
}

export default Dashboard;
