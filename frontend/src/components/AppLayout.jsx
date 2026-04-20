import { Link, Outlet, useNavigate } from "react-router-dom";
import { clearAuth, getStoredAuth } from "../auth";

function AppLayout() {
  const navigate = useNavigate();
  const { role } = getStoredAuth();

  const logout = () => {
    clearAuth();
    navigate("/login");
  };

  return (
    <div className="app-shell">
      <header className="top-nav">
        <h1>FurFinds</h1>
        <p className="tagline">Find. Adopt. Love.</p>
      </header>
      <nav className="nav-links">
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/pets">Pets</Link>
        <Link to="/add-pet">Add Pet</Link>
        <Link to="/analytics">Analytics</Link>
        <Link to="/ai-recommendation">AI Recommendation</Link>
        {role === "admin" ? <Link to="/admin">Admin</Link> : null}
        <button type="button" onClick={logout}>
          Logout
        </button>
      </nav>
      <main className="page-container">
        <Outlet />
      </main>
    </div>
  );
}

export default AppLayout;
