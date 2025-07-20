import { useEffect, useState } from "react";
import { submitLabAnswer } from "../utils/api";

export default function LabPage() {
  // state to store the lab data fetched from the backend
  const [lab, setLab] = useState(null);

  // track selected answer, submission status, and feedback message
  const [selectedAnswer, setSelectedAnswer] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [feedback, setFeedback] = useState("");

  // lab ID you want to fetch (you can later make this dynamic via routing)
  const labId = 1;
  // fetch the lab from the backend when the page loads
  useEffect(() => {
    async function fetchLab() {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/lab/${labId}`);
        const data = await res.json();
        setLab(data); // store in state
      } catch (err) {
        console.error("Failed to fetch lab:", err);
      }
    }

    fetchLab();
  }, [labId]); // re-run if labId ever changes

  // submit the user's selected answer to backend for scoring
  const handleSubmit = async () => {
    try {
      const res = await submitLabAnswer({
        userId: "demo", // replace with actual user ID later
        labId: labId,
        answer: selectedAnswer,
      });

      setFeedback(res.correct ? "✅ Correct!" : "❌ Incorrect.");
      setSubmitted(true);
    } catch (err) {
      console.error(err);
      setFeedback("!Error submitting answer!");
    }
  };

  // wait for lab data to load before rendering
  if (!lab) return <div className="p-4">Loading lab...</div>;

  return (
    <div className="p-4">
      {/* display title */}
      <h1 className="text-xl font-bold mb-2">{lab.title}</h1>

      {/* display log content inside a styled box */}
      <pre className="bg-gray-800 text-green-300 p-3 rounded mb-4 overflow-x-auto text-sm">
        {lab.log_data}
      </pre>

      {/* display the actual question */}
      <p className="mb-2">{lab.question}</p>

      {/* render each choice as a radio button */}
      <div className="mb-4">
        {lab.choices.map((option) => (
          <div key={option} className="mb-1">
            <label>
              <input
                type="radio"
                name="answer"
                value={option}
                onChange={() => setSelectedAnswer(option)}
                disabled={submitted}
              />
              <span className="ml-2">{option}</span>
            </label>
          </div>
        ))}
      </div>

      {/* submit button */}
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded"
        onClick={handleSubmit}
        disabled={submitted || !selectedAnswer}
      >
        Submit
      </button>

      {/* show feedback message after submission */}
      {submitted && <p className="mt-4 font-semibold">{feedback}</p>}
    </div>
  );
}
