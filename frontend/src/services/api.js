import axios from "axios";

const api = axios.create({
    // Vite proxies this local path to FastAPI. Keeping requests same-origin
    // makes the HttpOnly login cookie reliable in Chrome during development.
    baseURL: import.meta.env.VITE_API_URL || "/api",
    withCredentials: true
});

const clearAuthState = () => {
    sessionStorage.removeItem("carepilot_authenticated");
};

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            clearAuthState();
            if (window.location.pathname !== "/login") window.location.href = "/login";
        }

        return Promise.reject(error);
    }
);

export default api;
