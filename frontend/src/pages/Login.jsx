// Login.jsx
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../utils/api"; // helper to send POST to /login

export default function Login() {
  // controlled input state for email & password
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // feedback states
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const navigate = useNavigate();

  // if already logged in, skip this page
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      navigate("/dashboard", { replace: true }); // replace so back button won’t go to /login
    }
  }, [navigate]);

  // form submit handler
  const handleSubmit = async (e) => {
    e.preventDefault(); // don't reload page
    setError("");
    setLoading(true);

    try {
      // 1) hit the api with current credentials
      const { token, user, error: loginError } = await loginUser({ email, password });

      // 2) handle error response from backend
      if (loginError || !token) {
        throw new Error(loginError || "invalid credentials");
      }

      // 3) persist auth in localStorage
      localStorage.setItem("token", token);
      localStorage.setItem("userEmail", user.email); // so navbar shows it

      // 4) redirect to dashboard
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(err.message || "login failed or user not found.");
    } finally {
      setLoading(false);
    }
  };

  // ui layout
  return (
    <div className="max-w-md mx-auto mt-16 p-6 bg-white rounded-lg shadow">
      <h1 className="text-2xl font-semibold mb-4">Login</h1>

      {/* error message */}
      {error && <p className="text-red-500 mb-2">{error}</p>}

      {/* login form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* email input */}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />

        {/* password input */}
        <input
          type={showPassword ? "text" : "password"}
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />

        {/* show/hide password toggle */}
        <div className="flex items-center space-x-2">
          <input
            type="checkbox"
            id="showPassword"
            checked={showPassword}
            onChange={() => setShowPassword(!showPassword)}
            className="w-4 h-4"
          />
        <label htmlFor="showPassword" className="text-sm text-gray-700">
            show password
          </label>
        </div>

        {/* submit button */}
        <button
          type="submit"
          disabled={loading}
          className={`w-full py-2 text-white rounded ${
            loading ? "bg-blue-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {loading ? "logging in…" : "log in"}
        </button>
      </form>
    </div>
  );
}
