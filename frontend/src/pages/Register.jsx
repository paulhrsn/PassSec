import { useState } from "react";
import { registerUser } from "../utils/api";
import { useNavigate } from "react-router-dom";

export default function Register() {
  //keep track of what the user types
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  //quick check to make sure the email looks valid
  const validateEmail = (email) => /\S+@\S+\.\S+/.test(email);

  //this runs when the form is submitted
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    //verify email format before sending
    if (!validateEmail(email)) {
      setError("Please enter a valid email address.");
      return;
    }

    // send registration data to the backend
    const res = await registerUser({ email, password });
    if (res.error) {
      setError(res.error);
    } else {
      //on success, redirect to the login page
      navigate("/login");
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-semibold mb-4 text-center">Register</h1>

      {/* show any errors at the top */}
      {error && <div className="mb-4 text-red-600">{error}</div>}

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* email input */}
        <div>
          <label className="block text-sm font-medium mb-1">Email</label>
          <input
            type="email"  //browser-level validation for email format
            className="w-full border rounded px-3 py-2"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        {/* password input with show/hide toggle */}
        <div>
          <label className="block text-sm font-medium mb-1">Password</label>
          <input
            type={showPassword ? "text" : "password"}
            className="w-full border rounded px-3 py-2"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <label className="inline-flex items-center mt-1 text-sm">
            <input
              type="checkbox"
              checked={showPassword}
              onChange={() => setShowPassword((prev) => !prev)}
              className="mr-2"
            />
            Show Password
          </label>
        </div>

        {/* submit button */}
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Register
        </button>
      </form>
    </div>
  );
}

