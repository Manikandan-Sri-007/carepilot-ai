import { NavLink } from "react-router-dom";

const links = [
    { to: "/dashboard", label: "Dashboard" },
    { to: "/symptoms", label: "Symptom analysis" },
    { to: "/reports", label: "Report analysis" },
    { to: "/history", label: "History" },
    { to: "/profile", label: "Profile" }
];

function Sidebar() {
    return (
        <aside className="sidebar">
            <div className="sidebar-brand">
                <h3 className="text-xl font-semibold">🩺 CarePilot AI</h3>
                <p className="mt-2 text-sm text-slate-300">Care planning workspace</p>
            </div>

            <nav className="sidebar-nav">
                {links.map((link) => (
                    <NavLink
                        key={link.to}
                        to={link.to}
                        className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
                    >
                        {link.label}
                    </NavLink>
                ))}
            </nav>
        </aside>
    );
}

export default Sidebar;
