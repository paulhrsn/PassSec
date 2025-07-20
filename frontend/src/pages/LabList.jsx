import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchAllLabs } from "../utils/api";

export default function LabList() {
  const [labs, setLabs] = useState([]);

  useEffect(() => {
    fetchAllLabs()
      .then(data => setLabs(data))
      .catch(err => console.error("Failed to load labs:", err));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Cybersecurity Labs</h1>
      <ul className="space-y-2">
        {labs.map(lab => (
          <li key={lab.id}>
            <Link
              to={`/labs/${lab.id}`}
              className="block bg-gray-800 text-white p-4 rounded hover:bg-gray-700"
            >
              {lab.title}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
