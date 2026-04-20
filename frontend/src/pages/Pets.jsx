import { useCallback, useEffect, useMemo, useState } from "react";
import { adoptPet, extractErrorMessage, getPets, WS_BASE_URL } from "../api";

const CITY_OPTIONS = ["Chennai", "Coimbatore", "Madurai", "Erode", "Salem"];

function Pets() {
  const [pets, setPets] = useState([]);
  const [query, setQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [filters, setFilters] = useState({
    type: "",
    breed: "",
    age: "",
    gender: "",
    vaccinated: "",
    sterilized: "",
    city: "",
  });
  const [error, setError] = useState("");

  const loadPets = useCallback(async (activeFilters = filters) => {
    try {
      const params = {};
      if (activeFilters.type) params.type = activeFilters.type;
      if (activeFilters.breed) params.breed = activeFilters.breed;
      if (activeFilters.age) params.age = activeFilters.age;
      if (activeFilters.gender) params.gender = activeFilters.gender;
      if (activeFilters.city) params.city = activeFilters.city;
      if (activeFilters.vaccinated) params.vaccinated = activeFilters.vaccinated === "yes";
      if (activeFilters.sterilized) params.sterilized = activeFilters.sterilized === "yes";
      const response = await getPets(params);
      setPets(response.data);
      setError("");
    } catch (err) {
      setError(extractErrorMessage(err, "Failed to load pets."));
    }
  }, [filters]);

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      loadPets();
    }, 0);
    return () => clearTimeout(timeoutId);
  }, [loadPets]);

  useEffect(() => {
    const socket = new WebSocket(`${WS_BASE_URL}/ws`);
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
      setError("");
    } catch (err) {
      setError(extractErrorMessage(err, "Unable to adopt pet."));
    }
  };

  const filteredPets = useMemo(() => {
    const lowerQuery = query.toLowerCase();
    const toSearchable = (value) => String(value ?? "").toLowerCase();
    return pets.filter((pet) => {
      const matchesText =
        toSearchable(pet.name).includes(lowerQuery) ||
        toSearchable(pet.type).includes(lowerQuery) ||
        toSearchable(pet.breed).includes(lowerQuery) ||
        toSearchable(pet.city).includes(lowerQuery);
      const matchesStatus =
        statusFilter === "all" || (statusFilter === "adopted" ? pet.adopted : !pet.adopted);
      return matchesText && matchesStatus;
    });
  }, [pets, query, statusFilter]);

  const availablePets = useMemo(() => filteredPets.filter((pet) => !pet.adopted), [filteredPets]);
  const adoptedPets = useMemo(() => filteredPets.filter((pet) => pet.adopted), [filteredPets]);

  const clearFilters = () => {
    const cleared = {
      type: "",
      breed: "",
      age: "",
      gender: "",
      vaccinated: "",
      sterilized: "",
      city: "",
    };
    setFilters(cleared);
    setStatusFilter("all");
    setQuery("");
  };

  const renderPetItem = (pet, variant = "available") => {
    const descriptionPreview =
      pet.description && pet.description.length > 120
        ? `${pet.description.slice(0, 117)}...`
        : pet.description;

    const isAdopted = variant === "adopted";

    return (
      <li className={`pet-item pet-card ${isAdopted ? "pet-item-adopted" : "pet-item-available"}`} key={pet.id}>
        <img
          className="pet-image"
          src={pet.image_url || "https://placehold.co/220x140?text=FurFinds"}
          alt={pet.name}
        />
        <div className="pet-content">
          <h3>
            {pet.name} - {pet.type}
          </h3>
          <p className="pet-meta">
            {pet.breed} | {pet.age} | {pet.gender}
          </p>
          <p className="pet-meta">Location: {pet.city}</p>
          <p className="pet-meta">
            Health: {pet.vaccinated ? "Vaccinated" : "Not vaccinated"} /{" "}
            {pet.sterilized ? "Sterilized" : "Not sterilized"}
          </p>
          {descriptionPreview ? <p className="pet-meta">{descriptionPreview}</p> : null}
          <p className="pet-meta">
            Shelter: {pet.shelter_name} | Contact: {pet.contact_person}
          </p>
        </div>
        <button disabled={isAdopted || pet.adopted} onClick={() => adopt(pet.id)} type="button">
          {isAdopted || pet.adopted ? "Adopted" : "Adopt"}
        </button>
      </li>
    );
  };

  return (
    <section className="card">
      <h2>Pets</h2>
      <div className="row filter-row">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by name, type, breed, city"
        />
        <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
          <option value="all">All</option>
          <option value="available">Available</option>
          <option value="adopted">Adopted</option>
        </select>
      </div>
      <div className="form-grid filter-grid">
        <label>
          Type
          <select value={filters.type} onChange={(e) => setFilters((v) => ({ ...v, type: e.target.value }))}>
            <option value="">Any</option>
            <option value="Dog">Dog</option>
            <option value="Cat">Cat</option>
            <option value="Bird">Bird</option>
            <option value="Rabbit">Rabbit</option>
          </select>
        </label>
        <label>
          Breed
          <input
            value={filters.breed}
            onChange={(e) => setFilters((v) => ({ ...v, breed: e.target.value }))}
            placeholder="Any breed"
          />
        </label>
        <label>
          Age
          <select value={filters.age} onChange={(e) => setFilters((v) => ({ ...v, age: e.target.value }))}>
            <option value="">Any</option>
            <option value="Puppy">Puppy</option>
            <option value="Adult">Adult</option>
            <option value="Senior">Senior</option>
          </select>
        </label>
        <label>
          Gender
          <select value={filters.gender} onChange={(e) => setFilters((v) => ({ ...v, gender: e.target.value }))}>
            <option value="">Any</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>
        </label>
        <label>
          Vaccinated
          <select
            value={filters.vaccinated}
            onChange={(e) => setFilters((v) => ({ ...v, vaccinated: e.target.value }))}
          >
            <option value="">Any</option>
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        </label>
        <label>
          Sterilized
          <select
            value={filters.sterilized}
            onChange={(e) => setFilters((v) => ({ ...v, sterilized: e.target.value }))}
          >
            <option value="">Any</option>
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        </label>
        <label>
          City
          <select value={filters.city} onChange={(e) => setFilters((v) => ({ ...v, city: e.target.value }))}>
            <option value="">Any</option>
            {CITY_OPTIONS.map((city) => (
              <option key={city} value={city}>
                {city}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div className="row">
        <button type="button" onClick={clearFilters}>
          Clear Filters
        </button>
      </div>
      {error ? <p className="error-text">{error}</p> : null}
      {(statusFilter === "all" || statusFilter === "available") && (
        <div className="pet-section available-section">
          <h3 className="pet-section-title">Available Pets ({availablePets.length})</h3>
          <ul className="pet-list">{availablePets.map((pet) => renderPetItem(pet, "available"))}</ul>
        </div>
      )}
      {(statusFilter === "all" || statusFilter === "adopted") && (
        <div className="pet-section adopted-section">
          <h3 className="pet-section-title">Adopted Pets ({adoptedPets.length})</h3>
          <ul className="pet-list">{adoptedPets.map((pet) => renderPetItem(pet, "adopted"))}</ul>
        </div>
      )}
      {filteredPets.length === 0 ? <p className="helper-text">No pets found for current filters.</p> : null}
    </section>
  );
}

export default Pets;
