// src/pages/QuizPage.jsx

import { useEffect, useState } from "react";
import { fetchQuizQuestions, submitQuizAnswers } from "../utils/api";

export default function QuizPage() {
  // ────────────────────────────────
  // State declarations
  // ────────────────────────────────

  // Holds the list of questions fetched from the backend
  const [questions, setQuestions] = useState([]);

  // Tracks the user's selected answer for each question, keyed by question ID
  // e.g. { 3: "Phishing", 5: "Port Scanning" }
  const [selectedAnswers, setSelectedAnswers] = useState({});

  // After submission, holds { score, total } so we can display feedback
  const [feedback, setFeedback] = useState(null);

  // For the “start screen”: which domain to fetch questions from
  const [domain, setDomain]   = useState("Random");

  // How many questions to fetch
  const [count, setCount]     = useState(5);

  // Whether the quiz has started (i.e. we've fetched questions and are in "answering" mode)
  const [started, setStarted] = useState(false);


  // ────────────────────────────────
  // Handler: startQuiz
  // ────────────────────────────────
  // Fetches questions from the API using the selected domain/count,
  // initializes our state, and flips us into “quiz in progress” mode.
  const startQuiz = async () => {
    try {
      // Fetch the questions array from the server
      const qs = await fetchQuizQuestions({ domain, count });

      // Store them for rendering
      setQuestions(qs);

      // Reset any old answers/feedback
      setSelectedAnswers({});
      setFeedback(null);

      // Flip into the quiz view
      setStarted(true);
    } catch (err) {
      console.error("Error starting quiz:", err);
      // In production, show user a UI error here
    }
  };


  // ────────────────────────────────
  // Handler: handlePick
  // ────────────────────────────────
  // Called when the user picks an answer choice.
  // Updates `selectedAnswers` so that question `qid` maps to `choice`.
  const handlePick = (qid, choice) => {
    setSelectedAnswers(prev => ({
      ...prev,      // keep any existing answers
      [qid]: choice // override this question’s answer
    }));
  };


  // ────────────────────────────────
  // Handler: handleSubmit
  // ────────────────────────────────
  // Sends the user's answers to the API for scoring, then stores the result in `feedback`.
  const handleSubmit = async () => {
    try {
      // Build the payload format your backend expects:
      // [ { question_id: 3, answer: "Phishing" }, … ]
      const payload = questions.map(q => ({
        question_id: q.id,
        answer:      selectedAnswers[q.id] || ""
      }));

      // POST to /api/quiz/submit and destructure score & total
      const { score, total } = await submitQuizAnswers({ answers: payload });

      // Store feedback to show the user
      setFeedback({ score, total });
    } catch (err) {
      console.error("Quiz submission error:", err);
      // In production, surface a UI error here
    }
  };


  // ────────────────────────────────
  // Render
  // ────────────────────────────────
  return (
    <div className="max-w-3xl mx-auto p-6 space-y-8">

      {/* ─── Before starting: show domain/count inputs + Start button ─── */}
      {!started ? (
        <div className="bg-white shadow-lg rounded-lg p-6 grid gap-4 md:grid-cols-3">

          {/* Domain selector */}
          <div className="md:col-span-1">
            <label className="block text-gray-700 font-medium mb-1">
              Choose Domain
            </label>
            <select
              className="w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              value={domain}
              onChange={e => setDomain(e.target.value)}
            >
              <option>Random</option>
              <option>Attacks</option>
              <option>Architecture</option>
              <option>Implementation</option>
              {/* Add more domains as you seed them */}
            </select>
          </div>

          {/* Count input */}
          <div>
            <label className="block text-gray-700 font-medium mb-1">
              Number of Questions
            </label>
            <input
              type="number"
              min="1"
              max="50"
              className="w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              value={count}
              onChange={e => setCount(+e.target.value)}
            />
          </div>

          {/* Start button */}
          <div className="flex items-end">
            <button
              onClick={startQuiz}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded shadow"
            >
              Start Quiz
            </button>
          </div>
        </div>

      ) : (

        /* ─── Quiz in progress: render each question as a “card” ─── */
        <div className="space-y-6">
          {questions.map((q, idx) => (
            <div
              key={q.id}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
            >
              {/* Question text */}
              <p className="text-lg font-semibold mb-4">
                {idx + 1}. {q.question}
              </p>

              {/* Choices as radio buttons */}
              <div className="space-y-2">
                {q.choices.map(choice => (
                  <label
                    key={choice}
                    className="flex items-center space-x-3 cursor-pointer"
                  >
                    <input
                      type="radio"
                      name={`q-${q.id}`}                // group by question
                      className="text-blue-600 focus:ring-blue-500"
                      checked={selectedAnswers[q.id] === choice}
                      onChange={() => handlePick(q.id, choice)}
                    />
                    <span className="text-gray-800">{choice}</span>
                  </label>
                ))}
              </div>
            </div>
          ))}

          {/* ─── Action buttons: Reset & Submit ─── */}
          <div className="flex justify-end space-x-4">
            {/* Reset brings you back to the “start” screen */}
            <button
              onClick={() => setStarted(false)}
              className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded"
            >
              Reset
            </button>

            {/* Submit disabled until all answers are chosen */}
            <button
              onClick={handleSubmit}
              disabled={Object.keys(selectedAnswers).length < questions.length}
              className={`
                ${Object.keys(selectedAnswers).length < questions.length
                  ? "bg-green-300 cursor-not-allowed"
                  : "bg-green-600 hover:bg-green-700"}
                text-white font-semibold py-2 px-6 rounded shadow
              `}
            >
              Submit
            </button>
          </div>

          {/* ─── Feedback banner ─── */}
          {feedback && (
            <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded">
              <p className="text-green-800 font-medium text-center">
                ✅ You scored {feedback.score}/{feedback.total}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
