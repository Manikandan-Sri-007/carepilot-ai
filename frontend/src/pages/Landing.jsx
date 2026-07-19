import { motion } from "framer-motion";
import { Link } from "react-router-dom";

function Landing() {
    return (
        <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(37,99,235,0.14),_transparent_32%),linear-gradient(135deg,_#f8fbff_0%,_#eef5ff_100%)] px-4 py-8 text-slate-900 sm:px-6 lg:px-8">
            <div className="mx-auto flex max-w-7xl flex-col gap-8">
                <header className="glass-card flex items-center justify-between px-6 py-4">
                    <div>
                        <p className="eyebrow">CarePilot AI</p>
                        <h1 className="text-xl font-semibold">Your intelligent care companion</h1>
                    </div>
                    <div className="flex gap-3">
                        <Link to="/login" className="btn-secondary">Sign in</Link>
                        <Link to="/register" className="btn-primary">Create account</Link>
                    </div>
                </header>

                <main className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
                    <motion.section
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.45 }}
                        className="glass-card p-8 sm:p-10"
                    >
                        <p className="eyebrow">Trusted care guidance</p>
                        <h2 className="text-4xl font-semibold leading-tight sm:text-5xl">
                            Understand symptoms, reports, and next steps with calm, intelligent support.
                        </h2>
                        <p className="mt-4 max-w-2xl text-lg text-slate-600">
                            CarePilot AI brings symptom review, medical report insight, and guided recommendations into a secure, modern experience.
                        </p>
                        <div className="mt-6 flex flex-wrap gap-3">
                            <Link to="/register" className="btn-primary">Get started</Link>
                            <Link to="/login" className="btn-secondary">I already have an account</Link>
                        </div>
                        <div className="mt-8 grid gap-3 sm:grid-cols-3">
                            <div className="rounded-2xl border border-slate-200 bg-white/70 p-4">
                                <div className="text-2xl font-semibold text-brand-600">24/7</div>
                                <div className="text-sm text-slate-600">Guidance</div>
                            </div>
                            <div className="rounded-2xl border border-slate-200 bg-white/70 p-4">
                                <div className="text-2xl font-semibold text-brand-600">Secure</div>
                                <div className="text-sm text-slate-600">Protected history</div>
                            </div>
                            <div className="rounded-2xl border border-slate-200 bg-white/70 p-4">
                                <div className="text-2xl font-semibold text-brand-600">Modern</div>
                                <div className="text-sm text-slate-600">Clinical experience</div>
                            </div>
                        </div>
                    </motion.section>

                    <motion.section
                        initial={{ opacity: 0, y: 24 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.55 }}
                        className="glass-card p-8"
                    >
                        <div className="rounded-[28px] bg-slate-950 p-6 text-white shadow-glow">
                            <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Care overview</p>
                            <h3 className="mt-2 text-2xl font-semibold">Symptom review • Report insight • Care history</h3>
                            <div className="mt-6 space-y-3">
                                <div className="rounded-2xl border border-white/10 bg-white/10 p-4">
                                    <div className="text-sm text-slate-300">Latest insight</div>
                                    <div className="mt-1 font-semibold">Possible viral illness with moderate risk</div>
                                </div>
                                <div className="rounded-2xl border border-white/10 bg-white/10 p-4">
                                    <div className="text-sm text-slate-300">Recommended next step</div>
                                    <div className="mt-1 font-semibold">Rest, hydrate, and seek medical advice if symptoms persist</div>
                                </div>
                            </div>
                        </div>
                    </motion.section>
                </main>
            </div>
        </div>
    );
}

export default Landing;
