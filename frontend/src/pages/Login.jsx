//React hooks, router utilities
import { useState } from "react";
import { useNavigate } from "react-router-dom";
//api helper
import { loginUser } from "../utils/api"

export default function Login() {
    //1. component state

    const [email, setEmail] = useState(""); //controlled email input
    const [password, setPassword] = useState(""); //controlled password input
    const [error, setError] = useState(""); //holds login error msg
    const [loading, setLoading] = useState(false);//track if loading so we can disable button while it's submitting
    const [showPassword, setShowPassword] = useState(false); //add a show pw box

    //router hook, programmatically navigate on success
    const navigate = useNavigate();

    //form submit handler

    const handleSubmit = async (e) => {
        e.preventDefault(); //prevent full page reload
        setError("");
        setLoading(true);
        try {
            //call api helper w/ current credentials
            const { token, user, error: loginError } = await loginUser({ email, password });

            //if backend returns an error treat it as failure
        if (loginError) {
            throw new Error(loginError);
        }

        //successful login
        //persist session token in localstorage
        localStorage.setItem("token", token)
        //redirect user to dashboard
        navigate("/dashboard");
        } catch (err) {
            //on failure
            setError(err.message || "Login failed");
        } finally {
          setLoading(false)
        }
    };
    //jsx render
    return (
        <div className="max-w-md mx-auto mt-16 p-6 bg-white rounded-lg shadow">
          {/* page header */}
          <h1 className="text-2xl font-semibold mb-4">Login</h1>
    
          {/* show error message if present */}
          {error && <p className="text-red-500 mb-2">{error}</p>}
    
          {/* actual form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* email field */}
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}   // Update state on change
              className="w-full p-2 border rounded"
              required
            />
    
            {/* password field */}
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)} // Update state on change
              className="w-full p-2 border rounded"
              required
            />

          {/* toggle checkbox */}
        <div className="flex items-center space-x-2 mt-1">
          <input
            type="checkbox"
            id="showPassword"
            checked={showPassword}
            onChange={() => setShowPassword(!showPassword)}
            className="w-4 h-4"
          />
          <label htmlFor="showPassword" className="text-sm text-gray-700">
            Show Password
          </label>
        </div>
            {/* submit button */}
            <button
          type="submit"
          disabled={loading}  // Prevent double-clicks during login attempt
          className={`w-full py-2 text-white rounded 
            ${loading ? "bg-blue-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"}`}
        >
          {/* change button text while loading */}
          {loading ? "Logging in…" : "Log In"}
        </button>
      </form>
    </div>
  );
}