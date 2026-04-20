import { useEffect, useMemo, useState } from "react";
import { adoptPet, getPets } from "../api";

function Pets() {
  const [pets, setPets] = useState([]);
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState("all");
  const [error, setError] = useState("");

  const loadPets = async () => {
    try {
      const response = await getPets();
      setPets(response.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load pets.");
    }
  };

  useEffect(() => {
    loadPets();
  }, []);

  useEffect(() => {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws");
    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (payload?.event !== "pet_adopted") {
          return;
        }
        const adoptedId = payload?.pet?.id;
        setPets((current) =>
          current.map((pet) => (pet.id === adoptedId ? { ...pet, adopted: true } : pet))
        );
      } catch {
        // Ignore malformed realtime payloads.
      }
    };
    return () => socket.close();
  }, []);

  const adopt = async (id) => {
    try {
      await adoptPet(id);
      setPets((current) => current.map((pet) => (pet.id === id ? { ...pet, adopted: true } : pet)));
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to adopt pet.");
    }
  };

  const filteredPets = useMemo(() => {
    const lowerQuery = query.toLowerCase();
    return pets.filter((pet) => {
      const matchesText = pet.name.toLowerCase().includes(lowerQuery) || pet.type.toLowerCase().includes(lowerQuery);
      const matchesFilter =
        filter === "all" || (filter === "adopted" ? pet.adopted : !pet.adopted);
      return matchesText && matchesFilter;
    });
  }, [pets, query, filter]);

  return (
    <section className="card">
      <h2>Pets</h2>
      <div className="row">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by name or type"
        />
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">All</option>
          <option value="available">Available</option>
          <option value="adopted">Adopted</option>
        </select>
      </div>
      {error ? <p className="error-text">{error}</p> : null}
      <ul className="pet-list">
        {filteredPets.map((pet) => (
          <li className="pet-item" key={pet.id}>
            <div>
              <h3>{pet.name}</h3>
              <p className="pet-meta">Type: {pet.type}</p>
            </div>
            <button disabled={pet.adopted} onClick={() => adopt(pet.id)} type="button">
              {pet.adopted ? "Adopted" : "Adopt"}
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default Pets;
