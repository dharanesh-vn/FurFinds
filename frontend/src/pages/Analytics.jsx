import { useEffect, useState } from "react";
import { Bar, Doughnut } from "react-chartjs-2";
import { ArcElement, BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, Tooltip } from "chart.js";
import { extractErrorMessage, getAnalytics } from "../api";

ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

function Analytics() {
  const [data, setData] = useState({
    total_pets: 0,
    adopted_count: 0,
    adoption_rate: 0,
    by_type: {},
    by_city: {},
    vaccination: { vaccinated: 0, not_vaccinated: 0 },
    by_age: {},
  });
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const response = await getAnalytics();
        setData(response.data);
        setError("");
      } catch (err) {
        setError(extractErrorMessage(err, "Failed to load analytics."));
      }
    };
    load();
  }, []);

  const available = Math.max(data.total_pets - data.adopted_count, 0);
  const adoptionChartData = {
    labels: ["Adopted", "Available"],
    datasets: [
      {
        data: [data.adopted_count, available],
        backgroundColor: ["#ff6a00", "#ffd8bd"],
      },
    ],
  };
  const typeChartData = {
    labels: Object.keys(data.by_type || {}),
    datasets: [{ label: "Pets", data: Object.values(data.by_type || {}), backgroundColor: "#ff8f3f" }],
  };
  const cityChartData = {
    labels: ["Chennai", "Coimbatore", "Madurai", "Erode", "Salem", "Trichy", "Karur", "Tiruppur"],
    datasets: [
      {
        label: "Pets",
        data: ["Chennai", "Coimbatore", "Madurai", "Erode", "Salem", "Trichy", "Karur", "Tiruppur"].map(
          (city) => data.by_city?.[city] || 0
        ),
        backgroundColor: "#ffb075",
      },
    ],
  };
  const vaccinationChartData = {
    labels: ["Vaccinated", "Not Vaccinated"],
    datasets: [
      {
        data: [data.vaccination?.vaccinated || 0, data.vaccination?.not_vaccinated || 0],
        backgroundColor: ["#ff6a00", "#ffd8bd"],
      },
    ],
  };
  const ageChartData = {
    labels: Object.keys(data.by_age || {}),
    datasets: [{ label: "Pets", data: Object.values(data.by_age || {}), backgroundColor: "#ffc792" }],
  };

  return (
    <section className="card">
      <h2>Analytics</h2>
      <div className="stats-grid">
        <div className="stat-item">
          <h3>{data.total_pets}</h3>
          <p>Total Pets</p>
        </div>
        <div className="stat-item">
          <h3>{data.adopted_count}</h3>
          <p>Adopted</p>
        </div>
        <div className="stat-item">
          <h3>{(data.adoption_rate * 100).toFixed(1)}%</h3>
          <p>Adoption Rate</p>
        </div>
      </div>
      {error ? <p className="error-text">{error}</p> : null}
      <div className="chart-grid">
        <div className="chart-wrap card">
          <h3>Adoption Rate</h3>
          <p className="helper-text">Share of adopted pets vs available pets.</p>
          <Doughnut data={adoptionChartData} />
        </div>
        <div className="chart-wrap card">
          <h3>Pets by Type</h3>
          <p className="helper-text">Distribution across dogs, cats, birds, and more.</p>
          <Bar data={typeChartData} />
        </div>
        <div className="chart-wrap card">
          <h3>Pets by City (Tamil Nadu)</h3>
          <p className="helper-text">City-level inventory for all supported locations.</p>
          <Bar data={cityChartData} />
        </div>
        <div className="chart-wrap card">
          <h3>Vaccination Status</h3>
          <p className="helper-text">Vaccinated vs non-vaccinated pets.</p>
          <Doughnut data={vaccinationChartData} />
        </div>
        <div className="chart-wrap card">
          <h3>Age Distribution</h3>
          <p className="helper-text">Age buckets currently represented in listings.</p>
          <Bar data={ageChartData} />
        </div>
      </div>
    </section>
  );
}

export default Analytics;
