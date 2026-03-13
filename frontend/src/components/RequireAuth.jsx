import { useEffect, useState } from "react";
import { Navigate, useLocation } from "react-router-dom";
import { fetchCurrentUser } from "../utils/api";

export default function RequireAuth({ children }) {
  const [status, setStatus] = useState("checking");
  const token = localStorage.getItem("token"); // check if user is logged in
  const location = useLocation(); // current page path

  useEffect(() => {
    let mounted = true;

    async function verify() {
      if (!token) {
        if (mounted) setStatus("unauthorized");
        return;
      }
      try {
        const user = await fetchCurrentUser();
        localStorage.setItem("userEmail", user.email);
        if (mounted) setStatus("authorized");
      } catch {
        localStorage.removeItem("token");
        localStorage.removeItem("userEmail");
        if (mounted) setStatus("unauthorized");
      }
    }

    verify();
    return () => {
      mounted = false;
    };
  }, [token]);

  if (status === "checking") {
    return (
      <div className="min-h-[calc(100vh-64px)] bg-slate-950 text-slate-300 flex items-center justify-center">
        Verifying session...
      </div>
    );
  }

  if (!token || status === "unauthorized") {
    // not logged in then send to login, but remember where they were going
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // logged in then show the requested page
  return children;
}
