import { useState } from "react";
import { createPet } from "../api";

function AddPet() {
  const [name, setName] = useState("");
  const [type, setType] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    try {
      setError("");
      const response = await createPet({ name, type });
      setMessage(`Pet added: ${response.data.name}`);
      setName("");
      setType("");
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to add pet.");
    }
  };

  return (
    <section className="card">
      <h2>Add Pet</h2>
      <form className="stack" onSubmit={submit}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Pet name" />
        <input value={type} onChange={(e) => setType(e.target.value)} placeholder="Pet type" />
        <button type="submit">Add Pet</button>
      </form>
      {message ? <p className="helper-text">{message}</p> : null}
      {error ? <p className="error-text">{error}</p> : null}
    </section>
  );
}

export default AddPet;
