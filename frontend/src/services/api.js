import axios from "axios";

const configuredApiUrl = import.meta.env.VITE_API_URL?.trim();
const defaultApiUrl = import.meta.env.DEV
  ? "http://127.0.0.1:8000"
  : "https://carepilot-ai-1.onrender.com";

const baseURL = (configuredApiUrl || defaultApiUrl).replace(/\/$/, "");

export function getApiErrorMessage(error, fallback = "Request failed") {
  return error?.response?.data?.detail
    || error?.response?.data?.message
    || (error?.request ? "Network error: unable to reach CarePilot AI API" : "")
    || error?.message
    || fallback;
}

export function getAccessToken() {
  return localStorage.getItem("carepilot_access_token");
}

function getRefreshToken() {
  return localStorage.getItem("carepilot_refresh_token");
}

export function setTokens(accessToken, refreshToken) {
  localStorage.setItem("carepilot_access_token", accessToken);
  localStorage.setItem("carepilot_refresh_token", refreshToken);
}

export function clearTokens() {
  localStorage.removeItem("carepilot_access_token");
  localStorage.removeItem("carepilot_refresh_token");
}

const api = axios.create({
  baseURL,
  withCredentials: false,
});

let refreshPromise = null;

api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config || {};
    const status = error.response?.status;
    const requestUrl = originalRequest.url || "";
    const isAuthRoute = [
      "/auth/login",
      "/auth/register",
      "/auth/refresh",
      "/auth/forgot-password",
      "/auth/reset-password",
    ].some((path) => requestUrl.includes(path));

    if (status === 401 && !originalRequest._retry && !isAuthRoute) {
      originalRequest._retry = true;
      const refreshToken = getRefreshToken();
      if (!refreshToken) {
        clearTokens();
        return Promise.reject(error);
      }

      refreshPromise ||= api.post("/auth/refresh", { refresh_token: refreshToken })
        .then((res) => {
          setTokens(res.data.access_token, res.data.refresh_token);
          return res.data.access_token;
        })
        .catch((refreshError) => {
          clearTokens();
          throw refreshError;
        })
        .finally(() => {
          refreshPromise = null;
        });

      const newAccessToken = await refreshPromise;
      originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
      return api(originalRequest);
    }

    return Promise.reject(error);
  }
);

export default api;
