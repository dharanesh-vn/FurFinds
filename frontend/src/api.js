import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const getPets = () => api.get("/pets/");

export const createPet = (payload) => api.post("/pets/", payload);

export const adoptPet = (petId) => api.post(`/pets/${petId}/adopt`);

export default api;
