// src/pages/Dashboard.jsx
// Premium dashboard: stat cards + domain progress list + recharts bar chart

import { useEffect, useMemo, useState } from "react";
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

  const [userEmail, setUserEmail] = useState("");
  const [domainStats, setDomainStats] = useState([]); // [{domain, correct, total, percent}]
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const init = async () => {
      const stored = localStorage.getItem("userEmail");
      if (!stored) return navigate("/login");
      setUserEmail(stored);

      try {
        const stats = await fetchUserStats();
        stats.sort((a, b) => a.percent - b.percent); // weakest first
        setDomainStats(stats);
      } catch (e) {
        console.error("failed to load stats:", e);
        if (e.message === "Unauthorized") return navigate("/login");
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

  // ----- derived UI stats (for nice "stat cards") -----
  const summary = useMemo(() => {
    if (!domainStats.length) {
      return {
        totalAnswered: 0,
        overallAccuracy: 0,
        weakestDomain: null,
      };
    }

    const totalAnswered = domainStats.reduce((s, d) => s + (d.total || 0), 0);
    const totalCorrect = domainStats.reduce((s, d) => s + (d.correct || 0), 0);
    const overallAccuracy =
      totalAnswered > 0 ? Math.round((totalCorrect / totalAnswered) * 100) : 0;

    const weakestDomain = [...domainStats].sort((a, b) => a.percent - b.percent)[0];

    return { totalAnswered, overallAccuracy, weakestDomain };
  }, [domainStats]);

  // chart: keep weakest->strongest order but flip so chart reads top-to-bottom nicely
  const chartData = useMemo(() => {
    return [...domainStats]
      .sort((a, b) => a.percent - b.percent)
      .map(({ domain, percent }) => ({ domain, percent }));
  }, [domainStats]);

  const badgeForPercent = (percent) => {
    if (percent >= 80) return "bg-emerald-500/15 text-emerald-200 ring-1 ring-emerald-500/30";
    if (percent >= 50) return "bg-amber-500/15 text-amber-200 ring-1 ring-amber-500/30";
    return "bg-rose-500/15 text-rose-200 ring-1 ring-rose-500/30";
  };

  const labelForPercent = (percent) => {
    if (percent >= 80) return "Strong";
    if (percent >= 50) return "Improving";
    return "Needs work";
  };

  // shorten email for display (still available elsewhere)
  const displayEmail = userEmail.length > 28 ? userEmail.slice(0, 28) + "…" : userEmail;

  return (
    <div className="min-h-[calc(100vh-64px)] bg-slate-950">
      {/* page container */}
      <div className="max-w-6xl mx-auto px-4 py-10">
        {/* header */}
        <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-slate-400 text-sm">Dashboard</p>
            <h1 className="text-3xl md:text-4xl font-semibold text-white tracking-tight">
              Welcome back,{" "}
              <span className="text-sky-300">{displayEmail}</span>
            </h1>
            <p className="text-slate-400 mt-2 max-w-2xl">
              Your Security+ progress by domain, based on your quiz history.
            </p>
          </div>

          <div className="flex gap-3 mt-4 md:mt-0">
            <button
              onClick={() => navigate("/quiz")}
              className="px-4 py-2 rounded-xl bg-sky-500/15 text-sky-200 ring-1 ring-sky-500/25 hover:bg-sky-500/25 transition"
            >
              Take a Quiz
            </button>
            <button
              onClick={handleLogout}
              className="px-4 py-2 rounded-xl bg-white/5 text-slate-200 ring-1 ring-white/10 hover:bg-white/10 transition"
            >
              Log out
            </button>
          </div>
        </div>

        {/* loading */}
        {loading && (
          <div className="mt-10 rounded-2xl bg-white/5 ring-1 ring-white/10 p-8">
            <p className="text-slate-300">Loading your stats…</p>
          </div>
        )}

        {!loading && (
          <>
            {/* stat cards */}
            <div className="mt-10 grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 p-5">
                <p className="text-slate-400 text-sm">Total answered</p>
                <p className="text-3xl font-semibold text-white mt-1">
                  {summary.totalAnswered}
                </p>
                <p className="text-slate-400 text-sm mt-2">
                  Questions answered across all domains.
                </p>
              </div>

              <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 p-5">
                <p className="text-slate-400 text-sm">Overall accuracy</p>
                <p className="text-3xl font-semibold text-white mt-1">
                  {summary.overallAccuracy}%
                </p>
                <p className="text-slate-400 text-sm mt-2">
                  Weighted by total questions answered.
                </p>
              </div>

              <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 p-5">
                <p className="text-slate-400 text-sm">Weakest domain</p>
                <p className="text-xl font-semibold text-white mt-2">
                  {summary.weakestDomain ? summary.weakestDomain.domain : "—"}
                </p>
                <p className="text-slate-400 text-sm mt-2">
                  {summary.weakestDomain ? `${summary.weakestDomain.percent}% accuracy` : "Take a quiz to generate stats."}
                </p>
              </div>
            </div>

            {/* main content grid */}
            <div className="mt-6 grid grid-cols-1 lg:grid-cols-5 gap-6">
              {/* domain list */}
              <section className="lg:col-span-2 rounded-2xl bg-white/5 ring-1 ring-white/10 p-6">
                <div className="flex items-center justify-between">
                  <h2 className="text-white text-lg font-semibold">Domains</h2>
                  <span className="text-slate-400 text-sm">
                    Weak → Strong
                  </span>
                </div>

                {domainStats.length === 0 ? (
                  <div className="mt-5 rounded-xl bg-white/5 ring-1 ring-white/10 p-4">
                    <p className="text-slate-300">
                      Take a quiz to see your first stats.
                    </p>
                  </div>
                ) : (
                  <ul className="mt-5 space-y-3">
                    {domainStats.map(({ domain, percent, correct, total }, idx) => (
                      <li
                        key={domain}
                        className="rounded-xl bg-slate-900/40 ring-1 ring-white/10 p-4"
                      >
                        <div className="flex items-start justify-between gap-3">
                          <div>
                            <p className="text-white font-medium">
                              {idx + 1}. {domain}
                            </p>
                            <p className="text-slate-400 text-sm mt-1">
                              {correct}/{total} correct • {labelForPercent(percent)}
                            </p>
                          </div>

                          <div className={`shrink-0 px-3 py-1 rounded-full text-sm font-semibold ${badgeForPercent(percent)}`}>
                            {percent}%
                          </div>
                        </div>

                        {/* progress bar */}
                        <div className="mt-3 h-2 rounded-full bg-white/10 overflow-hidden">
                          <div
                            className="h-full bg-sky-400/70"
                            style={{ width: `${Math.max(0, Math.min(100, percent))}%` }}
                          />
                        </div>
                      </li>
                    ))}
                  </ul>
                )}
              </section>

              {/* chart */}
              <section className="lg:col-span-3 rounded-2xl bg-white/5 ring-1 ring-white/10 p-6">
                <div className="flex items-center justify-between">
                  <h2 className="text-white text-lg font-semibold">Progress</h2>
                  <span className="text-slate-400 text-sm">Accuracy by domain</span>
                </div>

                {domainStats.length === 0 ? (
                  <div className="mt-5 rounded-xl bg-white/5 ring-1 ring-white/10 p-4">
                    <p className="text-slate-300">
                      No chart yet — take a quiz to generate data.
                    </p>
                  </div>
                ) : (
                  <div className="mt-4 h-[340px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={chartData}
                        layout="vertical"
                        margin={{ top: 10, right: 40, left: 10, bottom: 10 }}
                      >
                        <XAxis type="number" domain={[0, 100]} hide />
                        <YAxis
                          type="category"
                          dataKey="domain"
                          width={140}
                          tick={{ fontSize: 12, fill: "#CBD5E1" }} // slate-300
                        />
                        <Tooltip
                          cursor={{ fill: "rgba(255,255,255,0.06)" }}
                          contentStyle={{
                            background: "rgba(2, 6, 23, 0.95)", // slate-950-ish
                            border: "1px solid rgba(255,255,255,0.12)",
                            borderRadius: 12,
                            color: "#E2E8F0",
                          }}
                          formatter={(v) => [`${v}%`, "Accuracy"]}
                        />
                        <Bar
                          dataKey="percent"
                          fill="#38BDF8" // sky-400
                          background={{ fill: "rgba(255,255,255,0.08)" }}
                          radius={[0, 10, 10, 0]}
                        >
                          <LabelList
                            dataKey="percent"
                            position="right"
                            formatter={(v) => `${v}%`}
                            fill="#E2E8F0"
                          />
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </section>
            </div>

            {/* footer hint */}
            <div className="mt-8 text-center text-slate-500 text-sm">
              Tip: Use “Take a Quiz” to keep your stats fresh.
            </div>
          </>
        )}
      </div>
    </div>
  );
}
