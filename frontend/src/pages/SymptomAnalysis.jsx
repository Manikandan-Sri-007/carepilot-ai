import { useState } from "react";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Toast from "../components/Toast";
import api from "../services/api";

function SymptomAnalysis() {
    const [symptoms, setSymptoms] = useState("");
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
            const response = await api.post("/analyze/symptoms", { symptoms });
            setResult(response.data);
            setToast("Analysis complete. Your AI summary is ready.");
        } catch (err) {
            setError("Unable to analyze symptoms right now. Please try again.");
            setToast("Unable to connect to the analysis service.");
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
                            <p className="eyebrow">Symptom analysis</p>
                            <h1 className="text-3xl font-semibold text-slate-900">Describe what you’re feeling</h1>
                            <p className="mt-2 text-slate-600">Share your symptoms and receive a practical AI-guided assessment.</p>
                        </div>
                    </section>

                    <form className="form-card" onSubmit={handleSubmit}>
                        <label className="form-label" htmlFor="symptoms">Symptoms</label>
                        <textarea
                            id="symptoms"
                            className="form-control"
                            rows="7"
                            value={symptoms}
                            onChange={(event) => setSymptoms(event.target.value)}
                            placeholder="Example: I have a fever and a cough for two days."
                            required
                        />

                        <button className="btn-primary" type="submit" disabled={loading}>
                            {loading ? "Analyzing..." : "Analyze symptoms"}
                        </button>
                    </form>

                    {error && <div className="result-card error">{error}</div>}

                    <Toast message={toast} type="info" onClose={() => setToast("")} />

                    {result && (
                        <div className="result-card space-y-3">
                            <h3 className="text-xl font-semibold text-slate-900">Assessment result</h3>
                            <p><strong>Possible disease:</strong> {result.possible_disease}</p>
                            <p><strong>Risk level:</strong> {result.risk_level}</p>
                            <p><strong>Explanation:</strong> {result.explanation}</p>
                            <p><strong>Recommendation:</strong> {result.recommendation}</p>
                            <div>
                                <strong>Follow-up questions:</strong>
                                <ul className="mt-2 list-disc pl-6 text-slate-600">
                                    {result.follow_up_questions?.map((question) => (
                                        <li key={question}>{question}</li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}

export default SymptomAnalysis;
