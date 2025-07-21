import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  //userEmail tracks whether someone is logged in (null if not)
  const [userEmail, setUserEmail] = useState(null);

  //toggle for dropdown menu when email is clicked
  const [menuOpen, setMenuOpen] = useState(false);

  //check localStorage on mount to see if a user is logged in
  useEffect(() => {
    const email = localStorage.getItem("userEmail");
    if (email) setUserEmail(email);
  }, []);

  //logout handler clears localStorage, resets state, and redirects
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userEmail");
    setUserEmail(null);
    setMenuOpen(false);
    navigate("/"); //take user back to login page
  };

  return (
    <nav className="flex items-center justify-between p-4 bg-gray-800 text-white">
      {/*app logo/title links to home*/}
      <Link to="/" className="text-lg font-bold">
        SecTrack
      </Link>

      <div className="flex items-center space-x-4">
        {userEmail ? (
          //if logged in, show email with dropdown menu
          <div className="relative">
            <button
              onClick={() => setMenuOpen(open => !open)}
              className="hover:underline focus:outline-none"
            >
              {userEmail}
            </button>

            {menuOpen && (
              <div className="absolute right-0 mt-2 w-32 bg-white text-gray-800 rounded shadow-lg">
                <button
                  onClick={handleLogout}
                  className="block w-full text-left px-4 py-2 hover:bg-gray-200"
                >
                  Log Out
                </button>
              </div>
            )}
          </div>
        ) : (
          //if not logged in, show login and register links
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
