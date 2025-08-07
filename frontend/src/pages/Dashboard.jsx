// src/pages/Dashboard.jsx
// shows %-correct per security+ domain + a simple bar chart

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  LabelList,
} from "recharts";
import { fetchUserStats } from "../utils/api";

export default function Dashboard() {
  const navigate = useNavigate();

  /** auth + data state */
  const [userEmail, setUserEmail] = useState("");
  const [domainStats, setDomainStats] = useState([]); //[{domain, correct, total, percent}]
  const [loading, setLoading] = useState(true);

  /** on mount, it verifies login and fetches stats */
  useEffect(() => {
    const init = async () => {
      const stored = localStorage.getItem("userEmail");
      if (!stored) {
        navigate("/login");
        return;
      }
      setUserEmail(stored);

      try {
        const stats = await fetchUserStats();
        //weakest domain first
        stats.sort((a, b) => a.percent - b.percent);
        setDomainStats(stats);
      } catch (e) {
        console.error("failed to load stats:", e);
        if (e.message === "Unauthorized") {
          // token was stale; userEmail was cleared by authFetch
          return navigate("/login");
        }
      } finally {
        setLoading(false);
      }
    };
    init();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  const chartData = domainStats.map(({ domain, percent }) => ({ domain, percent }));

  /* ui -------------------------------------------------------------------- */
  return (
    <div className="max-w-4xl mx-auto mt-16 p-6 bg-white rounded-lg shadow space-y-10">
      {/* ------------------------------------------------------------------ */}
      {/* header                                                            */}
      {/* ------------------------------------------------------------------ */}
      <header className="text-center space-y-1">
        <h1 className="text-3xl font-bold text-gray-800">
          Welcome, <span className="text-blue-600">{userEmail}</span>
        </h1>
        <p className="text-gray-600">Here are your Security+ scores, showing your accuracy in each domain you've answered questions from.</p>
      </header>

      {/* ------------------------------------------------------------------ */}
      {/* loading state                                                     */}
      {/* ------------------------------------------------------------------ */}
      {loading && <p className="text-gray-600 text-center">loading dashboard…</p>}

      {!loading && (
        <>
          {/* -------------------------------------------------------------- */}
          {/* domain list                                                   */}
          {/* -------------------------------------------------------------- */}
          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-gray-800">Your Domains</h2>

            {domainStats.length === 0 && (
              <p className="text-gray-600">
                Take a quiz or try a lab see your first stats!
              </p>
            )}

            <ul className="space-y-3">
              {domainStats.map(({ domain, percent }, idx) => {
                const badge =
                  percent >= 80
                    ? "bg-green-100 text-green-800"
                    : percent >= 50
                    ? "bg-yellow-100 text-yellow-800"
                    : "bg-red-100 text-red-800";
                return (
                  <li
                    key={domain}
                    className={`p-4 rounded border flex justify-between items-center ${badge}`}
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

          {/* -------------------------------------------------------------- */}
          {/* bar chart                                                     */}
          {/* -------------------------------------------------------------- */}
          {domainStats.length > 0 && (
            <section>
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
                  <Tooltip formatter={(v) => `${v}%`} />
                  <Bar
                    dataKey="percent"
                    fill="#3B82F6"
                    background={{ fill: "#E5E7EB" }}
                    radius={[0, 6, 6, 0]}
                  >
                    <LabelList
                      dataKey="percent"
                      position="right"
                      formatter={(v) => `${v}%`}
                    />
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </section>
          )}

          {/* -------------------------------------------------------------- */}
          {/* logout button                                                 */}
          {/* -------------------------------------------------------------- */}
          <button
            onClick={handleLogout}
            className="w-full py-2 bg-red-600 hover:bg-red-700 text-white rounded"
          >
            Log Out
          </button>
        </>
      )}
    </div>
  );
}
