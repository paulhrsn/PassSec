import { Navigate, useLocation } from "react-router-dom";

export default function RequireAuth({ children }) {
  const token = localStorage.getItem("token"); // check if user is logged in
  const location = useLocation(); // current page path

  if (!token) {
    // not logged in then send to login, but remember where they were going
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // logged in then show the requested page
  return children;
}
