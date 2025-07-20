import { useState } from "react";

// API function that sends POST to /api/lab/submit
import { submitLabAnswer } from "../utils/api";

export default function LabPage() {
  //track which answer the user has selected
  const [selectedAnswer, setSelectedAnswer] = useState("");

  //track whether the user has submitted already
  const [submitted, setSubmitted] = useState(false);

  //feedback message shown after submitting (correct / incorrect / error)
  const [feedback, setFeedback] = useState("");

  //runs when the user clicks "Submit"
  const handleSubmit = async () => {
    try {
      //Send answer to backend
      const res = await submitLabAnswer({
        userId: "demo", // hardcoded for now but will replace with real user ID later
        labId: "phishing-log-1", //to change depending on the lab
        answer: selectedAnswer, //user's selected answer
      });

      //based on server response, show either ✅ or ❌
      setFeedback(res.correct ? "✅ Correct!" : "❌ Incorrect.");
      setSubmitted(true); //prevent further submissions
    } catch (err) {
      console.error(err);
      setFeedback("!Error submitting answer!.");
    }
  };

  return (
    <div className="p-4">
      {/* lab title and question */}
      <h1 className="text-xl font-bold mb-4">Lab: Phishing Log Investigation</h1>
      <p className="mb-2">What kind of attack is shown in the log?</p>

      {/* render the answer choices as radio buttons */}
      <div className="mb-4">
        {[
          "Credential Harvesting",
          "SQL Injection",
          "Ransomware",
          "Man-in-the-Middle",
        ].map((option) => (
          <div key={option} className="mb-1">
            <label>
              <input
                type="radio"
                name="answer"
                value={option}
                //set selected answer when user clicks a radio option
                onChange={() => setSelectedAnswer(option)}
                disabled={submitted} //disable if already submitted
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
        disabled={submitted || !selectedAnswer} // Disable if no answer selected or already submitted
      >
        Submit
      </button>

      {/* display feedback after submission */}
      {submitted && <p className="mt-4 font-semibold">{feedback}</p>}
    </div>
  );
}
