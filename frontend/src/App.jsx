import { useEffect, useState } from "react";
import { adoptPet, createPet, getPets } from "./api";
import "./App.css";

function App() {
  const [pets, setPets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [name, setName] = useState("");
  const [type, setType] = useState("");

  const loadPets = async () => {
    try {
      setLoading(true);
      setError("");
      const response = await getPets();
      setPets(response.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load pets.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPets();
  }, []);

  const handleAdopt = async (petId) => {
    try {
      setError("");
      await adoptPet(petId);
      setPets((currentPets) =>
        currentPets.map((pet) =>
          pet.id === petId ? { ...pet, adopted: true } : pet
        )
      );
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to adopt pet.");
      loadPets();
    }
  };

  const handleCreatePet = async (event) => {
    event.preventDefault();
    if (!name.trim() || !type.trim()) {
      setError("Name and type are required.");
      return;
    }

    try {
      setError("");
      const response = await createPet({ name: name.trim(), type: type.trim() });
      setPets((currentPets) => [...currentPets, response.data]);
      setName("");
      setType("");
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to create pet.");
    }
  };

  return (
    <main className="app">
      <section className="hero">
        <p className="tagline">Find. Adopt. Love.</p>
        <h1>FurFinds</h1>
      </section>

      <section className="card">
        <form className="create-form" onSubmit={handleCreatePet}>
          <input
            className="field-input"
            type="text"
            placeholder="Pet name"
            value={name}
            onChange={(event) => setName(event.target.value)}
          />
          <input
            className="field-input"
            type="text"
            placeholder="Pet type"
            value={type}
            onChange={(event) => setType(event.target.value)}
          />
          <button className="adopt-button" type="submit">
            Add Pet
          </button>
        </form>

        <div className="header-row">
          <h2>Pet List</h2>
          <button className="refresh-button" onClick={loadPets}>
            Refresh
          </button>
        </div>

        {error ? <p className="error-text">{error}</p> : null}
        {loading ? <p className="helper-text">Loading pets...</p> : null}

        {!loading && pets.length === 0 ? (
          <p className="helper-text">No pets available yet.</p>
        ) : (
          <ul className="pet-list">
            {pets.map((pet) => (
              <li className="pet-item" key={pet.id}>
                <div>
                  <h3>{pet.name}</h3>
                  <p className="pet-meta">Type: {pet.type}</p>
                  <p className={pet.adopted ? "status adopted" : "status open"}>
                    {pet.adopted ? "Adopted" : "Available"}
                  </p>
                </div>
                <button
                  className="adopt-button"
                  onClick={() => handleAdopt(pet.id)}
                  disabled={pet.adopted}
                >
                  {pet.adopted ? "Adopted" : "Adopt"}
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}

export default App;
