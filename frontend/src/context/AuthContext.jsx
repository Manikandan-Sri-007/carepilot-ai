import { createContext, useCallback, useEffect, useMemo, useState } from "react";

import api, { clearTokens, getAccessToken, setTokens } from "../services/api";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadProfile = useCallback(async () => {
    const token = getAccessToken();
    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }

    try {
      const { data } = await api.get("/users/profile");
      setUser(data);
    } catch {
      clearTokens();
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadProfile();
  }, [loadProfile]);

  const login = useCallback(async (email, password) => {
    const { data } = await api.post("/auth/login", { email, password });
    setTokens(data.access_token, data.refresh_token);
    await loadProfile();
    return data;
  }, [loadProfile]);

  const register = useCallback(async (payload) => {
    const { data } = await api.post("/auth/register", payload);
    setTokens(data.access_token, data.refresh_token);
    await loadProfile();
    return data;
  }, [loadProfile]);

  const logout = useCallback(async () => {
    const refreshToken = localStorage.getItem("carepilot_refresh_token");
    if (refreshToken) {
      try {
        await api.post("/auth/logout", { refresh_token: refreshToken });
      } catch {
        // ignore logout network errors
      }
    }

    clearTokens();
    setUser(null);
  }, []);

  const value = useMemo(() => ({
    user,
    loading,
    isAuthenticated: Boolean(user),
    login,
    register,
    logout,
    refreshProfile: loadProfile,
  }), [user, loading, login, register, logout, loadProfile]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
