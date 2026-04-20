import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
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

export const getPets = () => api.get("/pets/");

export const createPet = (payload) => api.post("/pets/", payload);

export const adoptPet = (petId) => api.post(`/pets/${petId}/adopt`);

export const recommendPets = (preferences, topK = 3) =>
  api.post("/pets/recommend", { preferences, top_k: topK });

export const getAnalytics = () => api.get("/analytics");

export const getAdminUsers = () => api.get("/admin/users");

export default api;
