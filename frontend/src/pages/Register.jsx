// src/pages/Register.jsx
import { useMemo, useState } from "react";
import { registerUser } from "../utils/api";
import { useNavigate, Link } from "react-router-dom";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const emailLooksValid = useMemo(() => /\S+@\S+\.\S+/.test(email), [email]);

  const passwordStrength = useMemo(() => {
    const len = password.length;
    if (!password) return { label: "", cls: "" };
    if (len >= 12) return { label: "Strong", cls: "text-emerald-200" };
    if (len >= 8) return { label: "Okay", cls: "text-amber-200" };
    return { label: "Weak", cls: "text-rose-200" };
  }, [password]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (!emailLooksValid) throw new Error("Please enter a valid email address.");
      if (password.length < 8) throw new Error("Password must be at least 8 characters.");

      const res = await registerUser({ email, password });
      if (res.error) throw new Error(res.error);

      navigate("/login");
    } catch (err) {
      setError(err.message || "Registration failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] bg-slate-950">
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="max-w-md mx-auto">
          <p className="text-slate-400 text-sm">Authentication</p>
          <h1 className="text-3xl font-semibold text-white tracking-tight mt-1">
            Create your account
          </h1>
          <p className="text-slate-400 mt-2">
            Register to start tracking your Security+ quiz performance.
          </p>

          <div className="mt-6 rounded-2xl bg-white/5 ring-1 ring-white/10 p-6">
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
                  className={`w-full rounded-xl bg-slate-900/50 text-slate-100 placeholder:text-slate-500 ring-1 px-3 py-2 focus:outline-none focus:ring-2
                    ${
                      email.length === 0
                        ? "ring-white/10 focus:ring-sky-400/40"
                        : emailLooksValid
                        ? "ring-emerald-500/20 focus:ring-emerald-500/30"
                        : "ring-rose-500/20 focus:ring-rose-500/30"
                    }`}
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
                {email.length > 0 && (
                  <p className={`text-xs mt-2 ${emailLooksValid ? "text-emerald-200" : "text-rose-200"}`}>
                    {emailLooksValid ? "Looks good." : "That email format looks off."}
                  </p>
                )}
              </div>

              {/* password */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <label className="block text-sm font-medium text-slate-200">
                    Password
                  </label>
                  {passwordStrength.label && (
                    <span className={`text-xs ${passwordStrength.cls}`}>
                      {passwordStrength.label}
                    </span>
                  )}
                </div>

                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="At least 8 characters"
                  className="w-full rounded-xl bg-slate-900/50 text-slate-100 placeholder:text-slate-500 ring-1 ring-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-sky-400/40"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />

                <label className="mt-3 inline-flex items-center gap-2 text-sm text-slate-300">
                  <input
                    type="checkbox"
                    checked={showPassword}
                    onChange={() => setShowPassword((prev) => !prev)}
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
                {loading ? "Creating account…" : "Register"}
              </button>

              <p className="text-sm text-slate-400 text-center pt-2">
                Already have an account?{" "}
                <Link to="/login" className="text-sky-300 hover:text-sky-200 underline">
                  Log in
                </Link>
              </p>
            </form>
          </div>

          <p className="text-xs text-slate-500 text-center mt-6">
            Your email is used as your account ID (shown in the navbar).
          </p>
        </div>
      </div>
    </div>
  );
}
