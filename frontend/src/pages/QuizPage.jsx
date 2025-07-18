import { useEffect, useState } from "react";
import { fetchQuizQuestions } from "../utils/api";

export default function QuizPage() {
  const [questions, setQuestions] = useState([]);

  useEffect(() => {
    fetchQuizQuestions().then(setQuestions).catch(console.error);
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Quiz Questions</h1>
      {questions.map((q, i) => (
        <div key={i} className="mb-4 p-4 border rounded">
          <p className="font-semibold">{q.question}</p>
          <ul className="list-disc pl-5">
            {q.choices.map((choice, idx) => (
              <li key={idx}>{choice}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
