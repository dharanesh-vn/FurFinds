import axios from "axios";

const normalizeBaseUrl = (value) => value?.trim().replace(/\/+$/, "");

export const API_BASE_URL =
  normalizeBaseUrl(import.meta.env.VITE_API_BASE_URL) || "http://127.0.0.1:8000";

export const WS_BASE_URL =
  normalizeBaseUrl(import.meta.env.VITE_WS_BASE_URL) ||
  API_BASE_URL.replace(/^http/i, "ws");

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const registerUser = (payload) => api.post("/auth/register", payload);

export const loginUser = (payload) => api.post("/auth/login", payload);

export const getPets = (params = {}) => api.get("/pets/", { params });

export const createPet = (payload) => api.post("/pets/", payload);

export const adoptPet = (petId) => api.post(`/pets/${petId}/adopt`);

export const recommendPets = (preferences, topK = 3) =>
  api.post("/pets/recommend", { preferences, top_k: topK });

export const getAnalytics = () => api.get("/analytics");

export const getAdminUsers = () => api.get("/admin/users");

export default api;
