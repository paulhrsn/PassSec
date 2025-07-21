// Dashboard.jsx
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

export default function Dashboard() {
  const navigate = useNavigate();
  const [userEmail, setUserEmail] = useState("");
  const [loading, setLoading] = useState(true);

  // 🔒 Simulated user progress data
  const [domainStats, setDomainStats] = useState([
    { domain: "Threats, Attacks & Vulnerabilities", correct: 14, total: 20 },
    { domain: "Architecture & Design", correct: 10, total: 20 },
    { domain: "Implementation", correct: 5, total: 20 },
    { domain: "Operations & Incident Response", correct: 13, total: 20 },
    { domain: "Governance, Risk & Compliance", correct: 18, total: 20 },
  ]);

  useEffect(() => {
    const storedEmail = localStorage.getItem("userEmail");
    if (!storedEmail) {
      navigate("/login");
    } else {
      setUserEmail(storedEmail);
    }
    setLoading(false);
  }, [navigate]);

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  // Sort domains by weakest % correct
  const sortedDomains = [...domainStats].sort(
    (a, b) => a.correct / a.total - b.correct / b.total
  );

  // Data for chart
  const chartData = sortedDomains.map(({ domain, correct, total }) => ({
    domain,
    percent: Math.round((correct / total) * 100),
  }));

  return (
    <div className="max-w-4xl mx-auto mt-16 p-6 bg-white rounded-lg shadow space-y-8">
      {loading ? (
        <p className="text-gray-600">Loading dashboard…</p>
      ) : (
        <>
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-800">
              Welcome, <span className="text-blue-600">{userEmail}</span>
            </h1>
            <p className="text-gray-600 mt-2">Here's your Security+ progress snapshot</p>
          </div>

          <div className="space-y-4">
            <h2 className="text-2xl font-semibold text-gray-800">Your Domains</h2>
            <ul className="space-y-3">
              {sortedDomains.map(({ domain, correct, total }, i) => {
                const percent = Math.round((correct / total) * 100);
                const color =
                  percent >= 80
                    ? "bg-green-100 text-green-800"
                    : percent >= 50
                    ? "bg-yellow-100 text-yellow-800"
                    : "bg-red-100 text-red-800";

                return (
                  <li
                    key={domain}
                    className={`p-4 rounded border flex justify-between items-center ${color}`}
                  >
                    <span className="font-medium">{i + 1}. {domain}</span>
                    <span className="font-semibold">{percent}%</span>
                  </li>
                );
              })}
            </ul>
          </div>

          <div className="mt-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Progress Chart</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <XAxis type="number" domain={[0, 100]} hide />
                <YAxis type="category" dataKey="domain" width={180} tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="percent" fill="#3B82F6" radius={[0, 6, 6, 0]}>
                  <LabelList dataKey="percent" position="right" formatter={(val) => `${val}%`} />
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

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