import { useEffect, useState } from "react";

function QuizPage() {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/quiz`)
      .then((res) => res.json())
      .then((data) => {
        setQuestions(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch quiz questions:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="p-4 text-gray-600">Loading questions...</div>;

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Security+ Quiz</h1>
      {questions.map((q) => (
        <div key={q.id} className="mb-6 border rounded p-4 shadow">
          <p className="font-semibold">{q.question}</p>
          <ul className="list-disc ml-6 mt-2">
            {q.choices.map((choice, index) => (
              <li key={index}>{choice}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

export default QuizPage;
