import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-gray-900 text-white px-6 py-4 shadow-md">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        {/* logo / title */}
        <Link to="/" className="text-xl font-bold hover:text-blue-400">
          PassSec
        </Link>

        {/* nav links */}
        <div className="space-x-4">
          <Link to="/quiz" className="hover:text-blue-400">
            Quiz
          </Link>
          <Link to="/labs" className="hover:text-blue-400">
            Labs
          </Link>
          <Link to="/dashboard" className="hover:text-blue-400">
            Dashboard
          </Link>
          <Link to="/register" className="hover:text-blue-400">
            Register
          </Link>
        </div>
      </div>
    </nav>
  );
}
