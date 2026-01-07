// src/components/Navbar.jsx
// Premium navbar: constrained width, active link styling, user pill

import { useEffect, useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";

function NavLink({ to, label, active }) {
  return (
    <Link
      to={to}
      className={`px-3 py-2 rounded-xl text-sm font-medium transition ${
        active
          ? "bg-white/10 text-white ring-1 ring-white/15"
          : "text-slate-300 hover:text-white hover:bg-white/5"
      }`}
    >
      {label}
    </Link>
  );
}

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();

  const [userEmail, setUserEmail] = useState(null);

  useEffect(() => {
    const syncAuthState = () => {
      const t = localStorage.getItem("token");
      const email = t ? localStorage.getItem("userEmail") : null;
      setUserEmail(email);
    };

    syncAuthState();
    window.addEventListener("storage", syncAuthState);
    return () => window.removeEventListener("storage", syncAuthState);
  }, [location]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userEmail");
    setUserEmail(null);
    navigate("/login");
  };

  const path = location.pathname;

  return (
    <nav className="sticky top-0 z-50 bg-slate-950/80 backdrop-blur border-b border-white/10">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* brand */}
        <Link to="/" className="flex items-center gap-2">
          <div className="h-9 w-9 rounded-xl bg-sky-400/20 ring-1 ring-sky-400/30 flex items-center justify-center">
            <span className="text-sky-300 font-bold">S</span>
          </div>
          <div className="leading-tight">
            <p className="text-white font-semibold tracking-tight">SecTrack</p>
            <p className="text-slate-400 text-xs -mt-0.5">Security+ Quiz Tracker</p>
          </div>
        </Link>

        {/* links */}
        <div className="flex items-center gap-2">
          {userEmail ? (
            <>
              <NavLink to="/quiz" label="Quizzes" active={path.startsWith("/quiz")} />
              <NavLink
                to="/dashboard"
                label="Dashboard"
                active={path.startsWith("/dashboard")}
              />

              <div className="hidden md:flex items-center gap-2 ml-2 px-3 py-2 rounded-xl bg-white/5 ring-1 ring-white/10">
                <div className="h-7 w-7 rounded-full bg-white/10 flex items-center justify-center text-slate-200 text-xs font-bold">
                  {userEmail?.[0]?.toUpperCase() || "U"}
                </div>
                <span className="text-slate-200 text-sm max-w-[220px] truncate">
                  {userEmail}
                </span>
              </div>

              <button
                onClick={handleLogout}
                className="ml-2 px-3 py-2 rounded-xl text-sm font-medium text-slate-200 bg-white/5 ring-1 ring-white/10 hover:bg-white/10 transition"
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login" label="Log in" active={path.startsWith("/login") || path === "/"} />
              <NavLink to="/register" label="Register" active={path.startsWith("/register")} />
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
