import { useEffect, useState } from "react";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import api from "../services/api";

function Profile() {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");
    const [formData, setFormData] = useState({
        age: "",
        gender: "",
        profile_details: ""
    });

    useEffect(() => {
        const loadProfile = async () => {
            try {
                setLoading(true);
                setError("");
                const response = await api.get("/profile");
                setProfile(response.data);
                setFormData({
                    age: response.data?.age ?? "",
                    gender: response.data?.gender ?? "",
                    profile_details: response.data?.profile_details ?? ""
                });
            } catch (err) {
                console.error(err);
                setError("Unable to load your profile right now.");
            } finally {
                setLoading(false);
            }
        };

        loadProfile();
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            setSaving(true);
            setError("");
            const payload = {
                age: formData.age ? Number(formData.age) : null,
                gender: formData.gender || null,
                profile_details: formData.profile_details || null
            };
            const response = await api.post("/profile", payload);
            setProfile(response.data);
            setFormData({
                age: response.data?.age ?? "",
                gender: response.data?.gender ?? "",
                profile_details: response.data?.profile_details ?? ""
            });
        } catch (err) {
            console.error(err);
            setError("Your profile could not be updated. Please try again.");
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="app-shell">
            <Sidebar />

            <main className="app-main">
                <Navbar />

                <div className="content">
                    <section className="hero-card compact dark-hero">
                        <div>
                            <p className="eyebrow">Profile</p>
                            <h1 className="text-3xl font-semibold text-white">Your account overview</h1>
                            <p className="mt-2 text-slate-300">Keep your details handy and stay connected to your CarePilot experience.</p>
                        </div>
                    </section>

                    <section className="glass-card p-6">
                        {loading ? (
                            <div className="text-slate-300">Loading your profile...</div>
                        ) : (
                            <>
                                {error ? <div className="mb-4 text-sm text-rose-300">{error}</div> : null}
                                <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
                                    <div className="space-y-3">
                                        <h3 className="text-xl font-semibold text-white">Profile details</h3>
                                        <div className="rounded-2xl border border-slate-700/70 bg-slate-900/60 p-4 text-sm text-slate-300">
                                            <p><span className="text-slate-400">Name:</span> {profile?.name || "Not Provided"}</p>
                                            <p><span className="text-slate-400">Email:</span> {profile?.email || "Not Provided"}</p>
                                            <p><span className="text-slate-400">Age:</span> {profile?.age ?? "Not provided"}</p>
                                            <p><span className="text-slate-400">Gender:</span> {profile?.gender || "Not provided"}</p>
                                        </div>
                                    </div>

                                    <form className="space-y-3" onSubmit={handleSubmit}>
                                        <h3 className="text-xl font-semibold text-white">Update your care profile</h3>
                                        <label className="block text-sm text-slate-300">
                                            <span className="mb-1 block">Age</span>
                                            <input
                                                className="form-control"
                                                type="number"
                                                min="0"
                                                value={formData.age}
                                                onChange={(event) => setFormData({ ...formData, age: event.target.value })}
                                            />
                                        </label>
                                        <label className="block text-sm text-slate-300">
                                            <span className="mb-1 block">Gender</span>
                                            <input
                                                className="form-control"
                                                type="text"
                                                value={formData.gender}
                                                onChange={(event) => setFormData({ ...formData, gender: event.target.value })}
                                            />
                                        </label>
                                        <label className="block text-sm text-slate-300">
                                            <span className="mb-1 block">Profile details</span>
                                            <textarea
                                                className="form-control min-h-[100px]"
                                                value={formData.profile_details}
                                                onChange={(event) => setFormData({ ...formData, profile_details: event.target.value })}
                                            />
                                        </label>
                                        <button className="btn-primary w-full" type="submit" disabled={saving}>
                                            {saving ? "Saving..." : "Save profile"}
                                        </button>
                                    </form>
                                </div>
                            </>
                        )}
                    </section>
                </div>
            </main>
        </div>
    );
}

export default Profile;
