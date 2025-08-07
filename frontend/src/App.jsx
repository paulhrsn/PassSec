import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Register from "./pages/Register";
import QuizPage from "./pages/QuizPage";
import LabPage from "./pages/LabPage";
import Dashboard from "./pages/Dashboard";
import React, { useEffect } from "react";
import { checkHealth } from "./utils/api";
import LabList from "./pages/LabList";
import RequireAuth from "./components/RequireAuth"; // <-- import the wrapper

function App() {
  useEffect(() => {
    checkHealth().then(console.log).catch(console.error);
  }, []);

  return (
    <Router>
      <Navbar />
      <div className="p-4">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/quiz" element={<QuizPage />} />
          <Route path="/labs" element={<LabList />} />
          <Route path="/labs/:labId" element={<LabPage />} />
          
          {/* protect dashboard so it only works if logged in */}
          <Route
            path="/dashboard"
            element={
              <RequireAuth>
                <Dashboard />
              </RequireAuth>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
