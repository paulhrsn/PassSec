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

    //router hook, programmatically navigate on success
    const navigate = useNavigate();

    //form submit handler

    const handleSubmit = async (e) => {
        e.preventDefault(); //prevent full page reload

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
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)} // Update state on change
              className="w-full p-2 border rounded"
              required
            />
    
            {/* submit button */}
            <button
              type="submit"
              className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Log In
            </button>
          </form>
        </div>
      );
    }
