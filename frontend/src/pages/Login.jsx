// src/pages/Login.jsx
import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { loginUser } from "../utils/api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) navigate("/dashboard", { replace: true });
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const { token, user, error: loginError } = await loginUser({ email, password });

      if (loginError || !token) throw new Error(loginError || "Invalid credentials.");

      localStorage.setItem("token", token);
      localStorage.setItem("userEmail", user.email);

      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(err.message || "Login failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] bg-slate-950">
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="max-w-md mx-auto">
          {/* header */}
          <p className="text-slate-400 text-sm">Authentication</p>
          <h1 className="text-3xl font-semibold text-white tracking-tight mt-1">
            Log in
          </h1>
          <p className="text-slate-400 mt-2">
            Welcome back. Continue tracking your Security+ progress.
          </p>

          {/* card */}
          <div className="mt-6 rounded-2xl bg-white/5 ring-1 ring-white/10 p-6">
            {/* error */}
            {error && (
              <div className="mb-4 rounded-xl bg-rose-500/10 ring-1 ring-rose-500/20 px-4 py-3 text-rose-200 text-sm">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* email */}
              <div>
                <label className="block text-sm font-medium text-slate-200 mb-2">
                  Email
                </label>
                <input
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full rounded-xl bg-slate-900/50 text-slate-100 placeholder:text-slate-500 ring-1 ring-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-sky-400/40"
                  required
                />
              </div>

              {/* password */}
              <div>
                <label className="block text-sm font-medium text-slate-200 mb-2">
                  Password
                </label>
                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full rounded-xl bg-slate-900/50 text-slate-100 placeholder:text-slate-500 ring-1 ring-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-sky-400/40"
                  required
                />

                <label className="mt-3 inline-flex items-center gap-2 text-sm text-slate-300">
                  <input
                    type="checkbox"
                    checked={showPassword}
                    onChange={() => setShowPassword((p) => !p)}
                    className="h-4 w-4 rounded border-white/20 bg-white/10"
                  />
                  Show password
                </label>
              </div>

              {/* submit */}
              <button
                type="submit"
                disabled={loading}
                className={`w-full px-4 py-2 rounded-xl font-semibold ring-1 transition
                  ${
                    loading
                      ? "bg-sky-500/10 text-sky-200 ring-sky-500/20 cursor-not-allowed"
                      : "bg-sky-500/15 text-sky-200 ring-sky-500/25 hover:bg-sky-500/25"
                  }`}
              >
                {loading ? "Logging in…" : "Log in"}
              </button>

              {/* footer */}
              <p className="text-sm text-slate-400 text-center pt-2">
                Don’t have an account?{" "}
                <Link to="/register" className="text-sky-300 hover:text-sky-200 underline">
                  Register
                </Link>
              </p>
            </form>
          </div>

          <p className="text-xs text-slate-500 text-center mt-6">
            Tip: Use a real email format — it’s your account identifier.
          </p>
        </div>
      </div>
    </div>
  );
}
