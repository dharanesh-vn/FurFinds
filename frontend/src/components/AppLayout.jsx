import { NavLink, Outlet, useNavigate } from "react-router-dom";
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
      <header className="app-header">
        <div>
          <h1>FurFinds</h1>
          <p className="tagline">Find. Adopt. Love.</p>
        </div>
      </header>
      <nav className="nav-links card">
        <NavLink to="/dashboard">Dashboard</NavLink>
        <NavLink to="/pets">Pets</NavLink>
        <NavLink to="/add-pet">Add Pet</NavLink>
        <NavLink to="/analytics">Analytics</NavLink>
        <NavLink to="/ai-recommendation">AI Recommendation</NavLink>
        {role === "admin" ? <NavLink to="/admin">Admin</NavLink> : null}
        <button type="button" className="button-link secondary" onClick={logout}>
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
