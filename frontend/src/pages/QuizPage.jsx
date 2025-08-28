// src/pages/QuizPage.jsx

import { useEffect, useState } from "react";
import { fetchQuizQuestions, submitQuizAnswers } from "../utils/api";

export default function QuizPage() {

  // holds the list of questions fetched from the backend
  const [questions, setQuestions] = useState([]);

  // tracks the user's selected answer for each question, keyed by question ID
  // e.g. { 3: "Phishing", 5: "Port Scanning" }
  const [selectedAnswers, setSelectedAnswers] = useState({});

  // after submission, holds:
  // { score: number, total: number, results: [{ question_id, correct, correct_answer, explanation }, …] }
  const [feedback, setFeedback] = useState(null);

  // start-screen controls: domain & count
  const [domain, setDomain]   = useState("Random");
  const [count, setCount]     = useState(5);

  // whether quiz is in progress
  const [started, setStarted] = useState(false);


  // startQuiz: fetch questions & reset state
  const startQuiz = async () => {
    try {
      const qs = await fetchQuizQuestions({ domain, count });
      setQuestions(qs);
      setSelectedAnswers({});
      setFeedback(null);
      setStarted(true);
    } catch (err) {
      console.error("Error starting quiz:", err);
    }
  };


  // handlePick: user selects a radio button
  const handlePick = (qid, choice) => {
    setSelectedAnswers(prev => ({
      ...prev,
      [qid]: choice
    }));
  };


  // handleSubmit: send answers, receive score+results
  const handleSubmit = async () => {
    try {
      const payload = questions.map(q => ({
        question_id: q.id,
        answer:      selectedAnswers[q.id] || ""
      }));

       // making sure domain isn’t undefined
    console.log("↗️ submitting payload:", { answers: payload, domain });

      // now expecting { score, total, results }
      const { score, total, results } = await submitQuizAnswers({
         answers: payload, 
         domain 
        });

      setFeedback({ score, total, results });
    } catch (err) {
      console.error("Quiz submission error:", err);
    }
  };



  return (
    <div className="max-w-3xl mx-auto p-6 space-y-8">

      {/*  start screen  */}
      {!started ? (
        <div className="bg-white shadow-lg rounded-lg p-6 grid gap-4 md:grid-cols-3">
          {/* domain selector */}
          <div className="md:col-span-1">
            <label className="block text-gray-700 font-medium mb-1">Choose Domain</label>
            <select
              className="w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              value={domain}
              onChange={e => setDomain(e.target.value)}
            >
              <option>Random</option>
              <option>Attacks</option>
              <option>Architecture</option>
              <option>Implementation</option>
              {/* other domains */}
            </select>
          </div>

          {/* count input */}
          <div>
            <label className="block text-gray-700 font-medium mb-1">Number of Questions</label>
            <input
              type="number"
              min="1"
              max="50"
              className="w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              value={count}
              onChange={e => setCount(+e.target.value)}
            />
          </div>

          {/* start button */}
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

        /*  quiz in progress  */
        <div className="space-y-6">
          {questions.map((q, idx) => {
            // find this question's result after submit
            const result = feedback?.results.find(r => r.question_id === q.id);

            return (
              <div
                key={q.id}
                className={`
                  bg-white rounded-lg shadow-md p-6 transition-shadow
                  ${result
                    ? result.correct
                      ? "border-2 border-green-300"
                      : "border-2 border-red-300"
                    : "hover:shadow-lg"}
                `}
              >
                {/* question */}
                <p className="text-lg font-semibold mb-4">
                  {idx + 1}. {q.question}
                </p>

                {/* choices */}
                <div className="space-y-2">
                  {q.choices.map(choice => (
                    <label
                      key={choice}
                      className="flex items-center space-x-3 cursor-pointer"
                    >
                      <input
                        type="radio"
                        name={`q-${q.id}`}
                        className="text-blue-600 focus:ring-blue-500"
                        checked={selectedAnswers[q.id] === choice}
                        onChange={() => handlePick(q.id, choice)}
                        disabled={!!feedback}  
                      />
                      <span className="text-gray-800">{choice}</span>
                    </label>
                  ))}
                </div>

                {/* post-submit: correct/incorrect + explanation  */}
                {feedback && result && (
                  <div className="mt-4 space-y-1">
                    <p className={`font-semibold ${result.correct ? "text-green-600" : "text-red-600"}`}>
                      {result.correct ? "✅ Correct" : "❌ Incorrect"}
                    </p>
                    <p className="text-sm italic">
                      <span className="font-medium">Explanation:</span> {result.explanation}
                    </p>
                  </div>
                )}
              </div>
            );
          })}

          {/* reset & submit  */}
          <div className="flex justify-end space-x-4">
            <button
              onClick={() => setStarted(false)}
              className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded"
            >
              Reset
            </button>
            <button
              onClick={handleSubmit}
              disabled={Object.keys(selectedAnswers).length < questions.length || !!feedback}
              className={`
                ${Object.keys(selectedAnswers).length < questions.length || feedback
                  ? "bg-green-300 cursor-not-allowed"
                  : "bg-green-600 hover:bg-green-700"}
                text-white font-semibold py-2 px-6 rounded shadow
              `}
            >
              Submit
            </button>
          </div>

          {/* overall feedback banner */}
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
