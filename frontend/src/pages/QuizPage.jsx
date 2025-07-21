// src/pages/QuizPage.jsx

import { useEffect, useState } from "react";
import { fetchQuizQuestions, submitQuizAnswers } from "../utils/api";

export default function QuizPage() {


  //holds the list of questions fetched from the backend
  const [questions, setQuestions] = useState([]);

  //tracks the user's selected answer for each question, keyed by question ID
  // like 3: "Phishing", 5: "Port Scanning" }
  const [selectedAnswers, setSelectedAnswers] = useState({});

  //after submission, holds { score, total } so we can display feedback
  const [feedback, setFeedback] = useState(null);

  //for the “start screen”: which domain to fetch questions from
  const [domain, setDomain]   = useState("Random");

  //how many questions to fetch
  const [count, setCount]     = useState(5);

  //whether the quiz has started (i.e. we've fetched questions and are in "answering" mode)
  const [started, setStarted] = useState(false);



  const startQuiz = async () => {
    try {
      //fetch the questions array from the server
      const qs = await fetchQuizQuestions({ domain, count });

      //store them for rendering
      setQuestions(qs);

      //reset any old answers/feedback
      setSelectedAnswers({});
      setFeedback(null);

      //flip into the quiz view
      setStarted(true);
    } catch (err) {
      console.error("Error starting quiz:", err);
      //in production, show user a UI error here
    }
  };



  const handlePick = (qid, choice) => {
    setSelectedAnswers(prev => ({
      ...prev,      //keep any existing answers
      [qid]: choice //override this question’s answer
    }));
  };


  
  const handleSubmit = async () => {
    try {
      // build the payload format your backend expects:
      const payload = questions.map(q => ({
        question_id: q.id,
        answer:      selectedAnswers[q.id] || ""
      }));

      const { score, total } = await submitQuizAnswers({ answers: payload });

      //store feedback to show the user
      setFeedback({ score, total });
    } catch (err) {
      console.error("Quiz submission error:", err);
      //in production, surface a UI error here
    }
  };



  return (
    <div className="max-w-3xl mx-auto p-6 space-y-8">

      {/* before starting: show domain/count inputs + start button */}
      {!started ? (
        <div className="bg-white shadow-lg rounded-lg p-6 grid gap-4 md:grid-cols-3">

          {/*domain selector*/}
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

          {/*count input*/}
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

        /*quiz in progress: render each question as a “card”*/
        <div className="space-y-6">
          {questions.map((q, idx) => (
            <div
              key={q.id}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
            >
              {/* question text */}
              <p className="text-lg font-semibold mb-4">
                {idx + 1}. {q.question}
              </p>

              {/* choices as radio buttons */}
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

          {/*  action buttons: reset & submit  */}
          <div className="flex justify-end space-x-4">
            {/* reset brings you back to the “start” screen */}
            <button
              onClick={() => setStarted(false)}
              className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded"
            >
              Reset
            </button>

            {/* submit disabled until all answers are chosen */}
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

          {/* feedback banner */}
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
