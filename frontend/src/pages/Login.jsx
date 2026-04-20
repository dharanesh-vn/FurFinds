import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { loginUser } from "../api";
import { decodeTokenPayload } from "../auth";

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    try {
      setError("");
      const response = await loginUser({ email, password });
      const token = response.data.access_token;
      localStorage.setItem("token", token);
      const payload = decodeTokenPayload(token);
      if (payload?.role === "admin") {
        navigate("/admin");
      } else {
        navigate("/dashboard");
      }
    } catch (err) {
      setError(err?.response?.data?.detail || "Login failed.");
    }
  };

  return (
    <section className="card auth-card">
      <h2>Login</h2>
      <form onSubmit={submit} className="stack">
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          type="password"
        />
        <button type="submit">Login</button>
      </form>
      {error ? <p className="error-text">{error}</p> : null}
      <p>
        New user? <Link to="/register">Register</Link>
      </p>
    </section>
  );
}

export default Login;
