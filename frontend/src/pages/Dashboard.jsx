import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getAnalytics } from "../api";

function Dashboard() {
  const [analytics, setAnalytics] = useState({ total_pets: 0, adopted_count: 0, adoption_rate: 0 });

  useEffect(() => {
    const load = async () => {
      try {
        const response = await getAnalytics();
        setAnalytics(response.data);
      } catch {
        // Keep dashboard visible even if API fails.
      }
    };
    load();
  }, []);

  return (
    <section className="card">
      <h2>Dashboard</h2>
      <div className="stats-grid">
        <div className="stat-item">
          <h3>{analytics.total_pets}</h3>
          <p>Total Pets</p>
        </div>
        <div className="stat-item">
          <h3>{analytics.adopted_count}</h3>
          <p>Adopted</p>
        </div>
        <div className="stat-item">
          <h3>{analytics.total_pets - analytics.adopted_count}</h3>
          <p>Available</p>
        </div>
      </div>
      <div className="quick-links">
        <Link to="/pets">Pets</Link>
        <Link to="/add-pet">Add Pet</Link>
        <Link to="/analytics">Analytics</Link>
        <Link to="/ai-recommendation">AI Recommendation</Link>
      </div>
    </section>
  );
}

export default Dashboard;
