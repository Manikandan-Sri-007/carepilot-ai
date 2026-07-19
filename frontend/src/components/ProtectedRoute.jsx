import { Navigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

export default function ProtectedRoute({ children }) {
  const { loading, isAuthenticated } = useAuth();

  if (loading) {
    return <div className="grid min-h-screen place-items-center text-slate-600">Loading secure workspace...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
