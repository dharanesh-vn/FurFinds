import { useState } from "react";
import { recommendPets } from "../api";

function AIRecommendation() {
  const [preferences, setPreferences] = useState("");
  const [results, setResults] = useState([]);
  const [explanation, setExplanation] = useState("");
  const [error, setError] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    try {
      setError("");
      const response = await recommendPets(preferences, 3);
      setResults(response.data.recommendations);
      setExplanation(response.data.explanation);
    } catch (err) {
      setError(err?.response?.data?.detail || "Recommendation failed.");
    }
  };

  return (
    <section className="card">
      <h2>AI Recommendation</h2>
      <form className="row" onSubmit={submit}>
        <input
          value={preferences}
          onChange={(e) => setPreferences(e.target.value)}
          placeholder="small pet for apartment"
        />
        <button type="submit">Recommend</button>
      </form>
      {error ? <p className="error-text">{error}</p> : null}
      {explanation ? <p className="helper-text">{explanation}</p> : null}
      <ul className="pet-list">
        {results.map((pet) => (
          <li className="pet-item" key={pet.id}>
            <div>
              <h3>{pet.name}</h3>
              <p className="pet-meta">{pet.type}</p>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default AIRecommendation;
