import { useEffect, useState } from "react";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import api from "../services/api";

function History() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const loadHistory = async () => {
            try {
                const response = await api.get("/history");
                setItems(response.data);
            } catch (err) {
                setError("Unable to load your analysis history right now.");
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        loadHistory();
    }, []);

    return (
        <div className="app-shell">
            <Sidebar />

            <main className="app-main">
                <Navbar />

                <div className="content">
                    <section className="hero-card compact">
                        <div>
                            <p className="eyebrow">History</p>
                            <h1 className="text-3xl font-semibold text-slate-900">Your previous analyses</h1>
                            <p className="mt-2 text-slate-600">Review past symptom checks and report reviews whenever you need context.</p>
                        </div>
                    </section>

                    {loading && <div className="result-card">Loading your history...</div>}
                    {error && <div className="result-card error">{error}</div>}

                    {!loading && !error && items.length === 0 && (
                        <div className="result-card">No analyses yet. Start with your first symptom or report review.</div>
                    )}

                    <div className="history-list">
                        {items.map((item) => (
                            <div className="history-card" key={item.id}>
                                <div className="flex items-center justify-between gap-3">
                                    <span className="tag">{item.analysis_type}</span>
                                    <span className="muted">{item.created_at ? new Date(item.created_at).toLocaleDateString() : "Date not available"}</span>
                                </div>
                                <h3 className="mt-3 text-lg font-semibold text-slate-900">{item.analysis_type === "symptom" ? "Symptom analysis" : "Report analysis"}</h3>
                                <p className="mt-2 text-sm text-slate-600"><strong>Input:</strong> {item.input_text}</p>
                                <p className="mt-2 text-sm text-slate-600"><strong>Result:</strong> {item.result}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </main>
        </div>
    );
}

export default History;
