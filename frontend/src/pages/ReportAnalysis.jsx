import { useState } from "react";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Toast from "../components/Toast";
import api from "../services/api";

function ReportAnalysis() {
    const [reportText, setReportText] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [toast, setToast] = useState("");

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        setError("");
        setResult(null);
        setToast("");

        try {
            const response = await api.post("/analyze/report", { report_text: reportText });
            setResult(response.data);
            setToast("Report review complete.");
        } catch (err) {
            setError("Unable to process the report at the moment.");
            setToast("Unable to connect to the report analysis service.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-shell">
            <Sidebar />

            <main className="app-main">
                <Navbar />

                <div className="content">
                    <section className="hero-card compact">
                        <div>
                            <p className="eyebrow">Report analysis</p>
                            <h1 className="text-3xl font-semibold text-slate-900">Upload or paste your report</h1>
                            <p className="mt-2 text-slate-600">Review a concise summary and receive guidance based on the findings you provide.</p>
                        </div>
                    </section>

                    <form className="form-card" onSubmit={handleSubmit}>
                        <label className="form-label" htmlFor="report">Medical report text</label>
                        <div className="rounded-2xl border border-slate-200 bg-slate-50 p-3 text-sm text-slate-600">
                            Sample: glucose levels elevated, mild fatigue, and shortness of breath after exercise.
                        </div>
                        <textarea
                            id="report"
                            className="form-control"
                            rows="8"
                            value={reportText}
                            onChange={(event) => setReportText(event.target.value)}
                            placeholder="Paste lab notes, report summary, or diagnosis details here."
                            required
                        />

                        <button className="btn-primary" type="submit" disabled={loading}>
                            {loading ? "Reviewing report..." : "Analyze report"}
                        </button>
                    </form>

                    {error && <div className="result-card error">{error}</div>}

                    <Toast message={toast} type="info" onClose={() => setToast("")} />

                    {result && (
                        <div className="result-card space-y-3">
                            <h3 className="text-xl font-semibold text-slate-900">Report insight</h3>
                            <p><strong>Summary:</strong> {result.summary}</p>
                            <p><strong>Risk level:</strong> {result.risk_level}</p>
                            <p><strong>Recommendation:</strong> {result.recommendation}</p>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}

export default ReportAnalysis;
