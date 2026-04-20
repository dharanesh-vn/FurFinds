import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../api";

function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    city: "",
    password: "",
  });
  const [error, setError] = useState("");

  const update = (key, value) => setForm((current) => ({ ...current, [key]: value }));

  const submit = async (event) => {
    event.preventDefault();
    try {
      setError("");
      await registerUser(form);
      navigate("/login");
    } catch (err) {
      setError(err?.response?.data?.detail || "Registration failed.");
    }
  };

  return (
    <section className="card auth-card">
      <h2>Register</h2>
      <form onSubmit={submit} className="stack">
        <input value={form.name} onChange={(e) => update("name", e.target.value)} placeholder="Name" />
        <input
          value={form.email}
          onChange={(e) => update("email", e.target.value)}
          placeholder="Email"
        />
        <input
          value={form.phone}
          onChange={(e) => update("phone", e.target.value)}
          placeholder="Phone"
        />
        <input value={form.city} onChange={(e) => update("city", e.target.value)} placeholder="City" />
        <input
          value={form.password}
          onChange={(e) => update("password", e.target.value)}
          placeholder="Password"
          type="password"
        />
        <button type="submit">Create account</button>
      </form>
      {error ? <p className="error-text">{error}</p> : null}
      <p>
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </section>
  );
}

export default Register;
