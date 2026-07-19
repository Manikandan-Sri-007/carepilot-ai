import { useState } from "react";

import AppLayout from "../components/layout/AppLayout";
import api from "../services/api";

export default function AssistantPage() {
  const [message, setMessage] = useState("");
  const [conversation, setConversation] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const sendMessage = async () => {
    if (loading || !message.trim()) return;

    const userMessage = message;
    setMessage("");
    setConversation((prev) => [...prev, { role: "user", text: userMessage }]);
    setError("");
    setLoading(true);

    try {
      const { data } = await api.post("/chat", { message: userMessage });
      setConversation((prev) => [...prev, { role: "assistant", text: data.response }]);
    } catch (err) {
      setConversation((prev) => [...prev, { role: "assistant", text: "The assistant is temporarily unavailable. Please try again later." }]);
      setError(err?.response?.data?.detail || "Unable to reach the assistant right now.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppLayout>
      <div className="mx-auto flex h-[75vh] max-w-4xl flex-col rounded-2xl border border-slate-200 bg-white/80 p-4 dark:border-slate-800 dark:bg-slate-900/70">
        <h1 className="text-2xl font-semibold">AI Health Assistant</h1>
        <p className="text-sm text-slate-500">Ask health questions and clarify medical terms. LLM provider integration can be attached later in service layer.</p>

        <div className="mt-4 flex-1 space-y-3 overflow-y-auto rounded-xl bg-slate-50 p-3 dark:bg-slate-950/40">
          {conversation.map((item, index) => (
            <div key={`${item.role}-${index}`} className={`max-w-[80%] rounded-xl px-3 py-2 text-sm whitespace-pre-line ${item.role === "user" ? "ml-auto bg-teal-600 text-white" : "bg-white text-slate-800 dark:bg-slate-800 dark:text-slate-100"}`}>
              {item.text}
            </div>
          ))}

          {loading && (
            <div className="max-w-[80%] rounded-xl border border-teal-200 bg-teal-50 px-3 py-2 text-sm text-teal-700 dark:border-teal-900/60 dark:bg-teal-950/40 dark:text-teal-300">
              <div className="flex items-center gap-2">
                <span className="inline-flex h-2.5 w-2.5 animate-pulse rounded-full bg-teal-500" />
                <span>CarePilot AI is thinking about your message…</span>
              </div>
            </div>
          )}
        </div>

        {error && <div className="mt-3 rounded-xl bg-red-50 p-3 text-sm text-red-700">{error}</div>}

        <div className="mt-3 flex gap-2">
          <input value={message} onChange={(e) => setMessage(e.target.value)} onKeyDown={(e) => e.key === "Enter" && sendMessage()} className="w-full rounded-xl border border-slate-300 px-3 py-2 dark:border-slate-700 dark:bg-slate-800" placeholder="Ask a health question" />
          <button disabled={loading} onClick={sendMessage} className="rounded-xl bg-teal-600 px-4 py-2 font-semibold text-white hover:bg-teal-700 disabled:opacity-60">{loading ? "Sending..." : "Send"}</button>
        </div>
      </div>
    </AppLayout>
  );
}
