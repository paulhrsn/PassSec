// src/pages/LabList.jsx
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchAllLabs } from "../utils/api"; // custom function to GET /api/labs

export default function LabList() {
  const [labs, setLabs] = useState([]);

  // Fetch all lab metadata when the component mounts
  useEffect(() => {
    fetchAllLabs()
      .then((data) => setLabs(data))
      .catch((err) => {
        console.error("Failed to fetch labs:", err);
        setLabs([]);
      });
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Available Lab Scenarios</h1>

      {/* if no labs were loaded */}
      {labs.length === 0 ? (
        <p>No labs available.</p>
      ) : (
        <ul className="space-y-2">
          {labs.map((lab) => (
            <li key={lab.id}>
              {/* each lab title links to /labs/:labId */}
              <Link
  to={`/labs/${lab.id}`}
  className="block bg-blue-100 rounded-lg p-4 shadow hover:bg-blue-200 transition"
>
  <div className="text-lg font-semibold text-blue-800">🔍 {lab.title}</div>
</Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
