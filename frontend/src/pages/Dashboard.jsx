import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LabelList,
} from "recharts";
import { fetchUserStats } from "../utils/api"; // helper to get stats per domain

export default function Dashboard() {
  const navigate = useNavigate();

  //hold the logged-in user's email
  const [userEmail, setUserEmail] = useState("");

  //track loading status (both auth check and data fetch)
  const [loading, setLoading] = useState(true);

  //hold aggregated stats, the array of { domain, correct, total, percent }
  const [domainStats, setDomainStats] = useState([]);

  //verify user is logged in, then fetch stats
  useEffect(() => {
    const initializeDashboard = async () => {
      const storedEmail = localStorage.getItem("userEmail");
      if (!storedEmail) { //if not logged in
        navigate("/login");
        return;
      }
      setUserEmail(storedEmail);

      //fetch real stats from backend
      try {
        const stats = await fetchUserStats();
        //sort domains by ascending percentage (weakest first)
        stats.sort((a, b) => a.percent - b.percent);
        setDomainStats(stats);
      } catch (err) {
        console.error("Failed to load dashboard stats:", err);
      } finally {
        setLoading(false);
      }
    };

    initializeDashboard();
  }, [navigate]);

  //handle user logout by clearing storage and redirectting
  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  //data transformed for the bar chart: [{ domain, percent }]
  const chartData = domainStats.map(({ domain, percent }) => ({ domain, percent }));

  return (
    <div className="max-w-4xl mx-auto mt-16 p-6 bg-white rounded-lg shadow space-y-8">
      {loading ? (
        <p className="text-gray-600">Loading dashboard…</p>
      ) : (
        <>
          <header className="text-center">
            <h1 className="text-3xl font-bold text-gray-800">
              Welcome, <span className="text-blue-600">{userEmail}</span>
            </h1>
            <p className="text-gray-600 mt-2">
              Here&rsquo;s your Security+ progress snapshot
            </p>
          </header>

          {/* summary list of domains with percentage badges */}
          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-gray-800">
              Your Domains
            </h2>
            <ul className="space-y-3">
              {domainStats.map(({ domain, correct, total, percent }, idx) => {
                //change badge color based on performance
                const colorClass =
                  percent >= 80
                    ? "bg-green-100 text-green-800"
                    : percent >= 50
                    ? "bg-yellow-100 text-yellow-800"
                    : "bg-red-100 text-red-800";

                return (
                  <li
                    key={domain}
                    className={`p-4 rounded border flex justify-between items-center ${colorClass}`}
                  >
                    <span className="font-medium">
                      {idx + 1}. {domain}
                    </span>
                    <span className="font-semibold">{percent}%</span>
                  </li>
                );
              })}
            </ul>
          </section>

          {/* bar chart visualization of progress */}
          <section className="mt-8">
  <h2 className="text-2xl font-semibold text-gray-800 mb-4">
    Progress Chart
  </h2>
  <ResponsiveContainer width="100%" height={300}>
    <BarChart
      data={chartData}
      layout="vertical"
      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
    >
      <XAxis type="number" domain={[0, 100]} hide />
      <YAxis
        type="category"
        dataKey="domain"
        width={180}
        tick={{ fontSize: 12 }}
      />
      <Tooltip formatter={(val) => `${val}%`} />
      <Bar
        dataKey="percent"
        fill="#3B82F6"
        background={{ fill: "#E5E7EB" }}
        radius={[0, 6, 6, 0]}
      >
        <LabelList
          dataKey="percent"
          position="right"
          formatter={(val) => `${val}%`}
        />
      </Bar>
    </BarChart>
  </ResponsiveContainer>
</section>

<button
  onClick={handleLogout}
  className="mt-8 w-full py-2 bg-red-600 hover:bg-red-700 text-white rounded"
>
  Log Out
</button>

        </>
      )}
    </div>
  );
}
