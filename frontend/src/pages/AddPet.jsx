import { useState } from "react";
import { createPet, extractErrorMessage } from "../api";

const initialForm = {
  name: "",
  type: "Dog",
  breed: "",
  age: "Adult",
  gender: "Male",
  vaccinated: true,
  sterilized: false,
  description: "",
  image_url: "",
  shelter_name: "",
  contact_person: "",
  phone: "+91",
  email: "",
  city: "Chennai",
};

function AddPet() {
  const [form, setForm] = useState(initialForm);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const setField = (field, value) => {
    setForm((current) => ({ ...current, [field]: value }));
  };

  const submit = async (event) => {
    event.preventDefault();
    if (!form.name.trim() || !form.type.trim() || !form.breed.trim() || !form.city.trim()) {
      setError("Please fill all required fields: name, type, breed, and city.");
      return;
    }

    try {
      setError("");
      const payload = {
        ...form,
        name: form.name.trim(),
        type: form.type.trim(),
        breed: form.breed.trim(),
        age: form.age.trim() || "Adult",
        city: form.city.trim(),
        description: form.description.trim() || null,
        image_url: form.image_url.trim() || null,
        shelter_name: form.shelter_name.trim() || null,
        contact_person: form.contact_person.trim() || null,
        phone: form.phone.trim() || null,
        email: form.email.trim() || null,
      };
      const response = await createPet(payload);
      setMessage(`Pet added: ${response.data.name}`);
      setForm(initialForm);
    } catch (err) {
      setError(extractErrorMessage(err, "Unable to add pet."));
    }
  };

  return (
    <section className="card">
      <h2>Add Pet</h2>
      <p className="helper-text">Fields marked with * are required.</p>
      <form className="stack" onSubmit={submit}>
        <div className="form-grid">
          <label>
            Pet Name *
            <input
              value={form.name}
              onChange={(e) => setField("name", e.target.value)}
              placeholder="e.g. Bruno"
              required
            />
          </label>

          <label>
            Type *
            <select value={form.type} onChange={(e) => setField("type", e.target.value)} required>
              <option>Dog</option>
              <option>Cat</option>
              <option>Rabbit</option>
              <option>Bird</option>
              <option>Other</option>
            </select>
          </label>

          <label>
            Breed *
            <input
              value={form.breed}
              onChange={(e) => setField("breed", e.target.value)}
              placeholder="e.g. Labrador Mix"
              required
            />
          </label>

          <label>
            Age
            <select value={form.age} onChange={(e) => setField("age", e.target.value)}>
              <option value="Puppy">Puppy</option>
              <option value="Adult">Adult</option>
              <option value="Senior">Senior</option>
            </select>
          </label>

          <fieldset className="radio-group">
            <legend>Gender</legend>
            <label>
              <input
                type="radio"
                name="gender"
                checked={form.gender === "Male"}
                onChange={() => setField("gender", "Male")}
              />
              Male
            </label>
            <label>
              <input
                type="radio"
                name="gender"
                checked={form.gender === "Female"}
                onChange={() => setField("gender", "Female")}
              />
              Female
            </label>
          </fieldset>

          <label>
            Vaccinated
            <select
              value={form.vaccinated ? "yes" : "no"}
              onChange={(e) => setField("vaccinated", e.target.value === "yes")}
            >
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </select>
          </label>

          <label>
            Sterilized
            <select
              value={form.sterilized ? "yes" : "no"}
              onChange={(e) => setField("sterilized", e.target.value === "yes")}
            >
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </select>
          </label>

          <label>
            City *
            <select value={form.city} onChange={(e) => setField("city", e.target.value)} required>
              <option value="Chennai">Chennai</option>
              <option value="Coimbatore">Coimbatore</option>
              <option value="Madurai">Madurai</option>
              <option value="Erode">Erode</option>
              <option value="Salem">Salem</option>
            </select>
          </label>

          <label>
            Shelter Name
            <input
              value={form.shelter_name}
              onChange={(e) => setField("shelter_name", e.target.value)}
              placeholder="e.g. FurFinds Downtown"
            />
          </label>

          <label>
            Contact Person
            <input
              value={form.contact_person}
              onChange={(e) => setField("contact_person", e.target.value)}
              placeholder="e.g. Priya"
            />
          </label>

          <label>
            Phone
            <input
              value={form.phone}
              onChange={(e) => setField("phone", e.target.value)}
              placeholder="e.g. +919876543210"
            />
          </label>

          <label>
            Email
            <input
              value={form.email}
              onChange={(e) => setField("email", e.target.value)}
              placeholder="e.g. shelter@furfinds.com"
              type="email"
            />
          </label>

          <label className="field-full">
            Image URL
            <input
              value={form.image_url}
              onChange={(e) => setField("image_url", e.target.value)}
              placeholder="https://..."
            />
          </label>

          <label className="field-full">
            Description
            <textarea
              value={form.description}
              onChange={(e) => setField("description", e.target.value)}
              placeholder="Temperament, home preference, behavior notes..."
              rows={4}
            />
          </label>
        </div>
        <button type="submit">Add Pet</button>
      </form>
      {message ? <p className="helper-text">{message}</p> : null}
      {error ? <p className="error-text">{error}</p> : null}
    </section>
  );
}

export default AddPet;
