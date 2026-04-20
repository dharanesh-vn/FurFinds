import { useEffect, useState } from "react";
import { Doughnut } from "react-chartjs-2";
import { ArcElement, Chart as ChartJS, Legend, Tooltip } from "chart.js";
import { getAnalytics } from "../api";

ChartJS.register(ArcElement, Tooltip, Legend);

function Analytics() {
  const [data, setData] = useState({ total_pets: 0, adopted_count: 0, adoption_rate: 0 });

  useEffect(() => {
    const load = async () => {
      const response = await getAnalytics();
      setData(response.data);
    };
    load();
  }, []);

  const available = Math.max(data.total_pets - data.adopted_count, 0);
  const chartData = {
    labels: ["Adopted", "Available"],
    datasets: [
      {
        data: [data.adopted_count, available],
        backgroundColor: ["#ff6a00", "#ffd8bd"],
      },
    ],
  };

  return (
    <section className="card">
      <h2>Analytics</h2>
      <p>Total Pets: {data.total_pets}</p>
      <p>Adopted Count: {data.adopted_count}</p>
      <p>Adoption Rate: {(data.adoption_rate * 100).toFixed(1)}%</p>
      <div className="chart-wrap">
        <Doughnut data={chartData} />
      </div>
    </section>
  );
}

export default Analytics;
