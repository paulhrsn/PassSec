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
          <Route path="/register" element={<Register />} />
          <Route path="/quiz" element={<QuizPage />} />
          <Route path="/lab" element={<LabPage />} />
          <Route path="/labs" element={<LabList />} />
          <Route path="/labs/:labId" element={<LabPage />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </Router>
  );
}



export default App;
