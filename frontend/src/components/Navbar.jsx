import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Navbar() {
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            await api.post("/logout");
        } finally {
            sessionStorage.removeItem("carepilot_authenticated");
            sessionStorage.removeItem("carepilot_access_token");
            navigate("/login");
        }
    };

    return (
        <header className="topbar">
            <div>
                <p className="eyebrow">CarePilot AI</p>
                <h2 className="text-lg font-semibold text-white">Care workspace</h2>
            </div>

            <div className="topbar-actions">
                <button className="user-pill" onClick={() => navigate("/profile")}>Profile</button>
                <button className="btn-outline" onClick={handleLogout}>
                    Logout
                </button>
            </div>
        </header>
    );
}

export default Navbar;
