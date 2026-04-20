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
    labels: ["Chennai", "Coimbatore", "Madurai", "Erode", "Salem"],
    datasets: [
      {
        label: "Pets",
        data: ["Chennai", "Coimbatore", "Madurai", "Erode", "Salem"].map((city) => data.by_city?.[city] || 0),
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
      <p>Total Pets: {data.total_pets}</p>
      <p>Adopted Count: {data.adopted_count}</p>
      <p>Adoption Rate: {(data.adoption_rate * 100).toFixed(1)}%</p>
      {error ? <p className="error-text">{error}</p> : null}
      <div className="chart-grid">
        <div className="chart-wrap">
          <h3>Adoption Rate</h3>
          <Doughnut data={adoptionChartData} />
        </div>
        <div className="chart-wrap">
          <h3>Pets by Type</h3>
          <Bar data={typeChartData} />
        </div>
        <div className="chart-wrap">
          <h3>Pets by City (Tamil Nadu)</h3>
          <Bar data={cityChartData} />
        </div>
        <div className="chart-wrap">
          <h3>Vaccination Status</h3>
          <Doughnut data={vaccinationChartData} />
        </div>
        <div className="chart-wrap">
          <h3>Age Distribution</h3>
          <Bar data={ageChartData} />
        </div>
      </div>
    </section>
  );
}

export default Analytics;
