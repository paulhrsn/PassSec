import { useState, useEffect } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation(); // rerun effect when route changes

  // holds the logged‑in user email (null when logged out)
  const [userEmail, setUserEmail] = useState(null);

  // keep userEmail in sync with localStorage
  useEffect(() => {
    const syncAuthState = () => {
    const t = localStorage.getItem("token");
    const email = t ? localStorage.getItem("userEmail") : null;
      setUserEmail(localStorage.getItem("userEmail"));
    };

    // run once immediately
    syncAuthState();

    // update when url changes 
    // and when any other tab modifies localStorage (storage event)
    window.addEventListener("storage", syncAuthState);

    return () => {
      window.removeEventListener("storage", syncAuthState);
    };
  }, [location]);

  // log the user out and return to login page
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userEmail");
    setUserEmail(null);
    navigate("/");
  };

  return (
    <nav className="flex items-center justify-between p-4 bg-gray-800 text-white">
      {/* brand / home link */}
      <Link to="/" className="text-lg font-bold">
        SecTrack
      </Link>

      <div className="flex items-center space-x-6">
        {/*  logged‑in view  */}
        {userEmail ? (
          <>
            {/* main app links */}
            <Link to="/quiz" className="hover:underline">
              Quizzes
            </Link>
            <Link to="/labs" className="hover:underline">
              Labs
            </Link>
            <Link to="/dashboard" className="hover:underline">
            Dashboard
            </Link>

            {/* user email (plain text) */}
            <span>{userEmail}</span>

            {/* logout button */}
            <button onClick={handleLogout} className="hover:underline">
              Log Out
            </button>
          </>
        ) : (
          /*  logged‑out view  */
          <>
            <Link to="/" className="hover:underline">
              Log In
            </Link>
            <Link to="/register" className="hover:underline">
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
