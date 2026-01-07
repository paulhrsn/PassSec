// src/pages/QuizPage.jsx
// Premium Quiz UI (dark theme): start panel + question cards + selectable options + results summary

import { useMemo, useState } from "react";
import { fetchQuizQuestions, submitQuizAnswers } from "../utils/api";

function OptionRow({ label, selected, disabled, onClick, state }) {
  // state: "neutral" | "correct" | "wrong"
  const base =
    "w-full text-left flex items-start gap-3 rounded-xl px-4 py-3 ring-1 transition";
  const neutral =
    "bg-white/5 ring-white/10 hover:bg-white/10 hover:ring-white/20";
  const selectedStyle = "ring-sky-400/40 bg-sky-400/10";
  const correctStyle = "ring-emerald-500/40 bg-emerald-500/10";
  const wrongStyle = "ring-rose-500/40 bg-rose-500/10";
  const disabledStyle = "opacity-80 cursor-not-allowed";

  const cls = [
    base,
    neutral,
    selected ? selectedStyle : "",
    state === "correct" ? correctStyle : "",
    state === "wrong" ? wrongStyle : "",
    disabled ? disabledStyle : "cursor-pointer",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <button type="button" className={cls} onClick={onClick} disabled={disabled}>
      <span
        className={[
          "mt-1 h-4 w-4 shrink-0 rounded-full ring-1",
          selected ? "bg-sky-300/80 ring-sky-300/60" : "bg-white/5 ring-white/20",
        ].join(" ")}
      />
      <span className="text-slate-100 leading-snug">{label}</span>
    </button>
  );
}

export default function QuizPage() {
  const [questions, setQuestions] = useState([]);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [feedback, setFeedback] = useState(null);

  const [domain, setDomain] = useState("Random");
  const [count, setCount] = useState(5);
  const [started, setStarted] = useState(false);
  const [starting, setStarting] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const startQuiz = async () => {
    try {
      setStarting(true);
      const qs = await fetchQuizQuestions({ domain, count });
      setQuestions(qs);
      setSelectedAnswers({});
      setFeedback(null);
      setStarted(true);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      console.error("Error starting quiz:", err);
    } finally {
      setStarting(false);
    }
  };

  const handlePick = (qid, choice) => {
    setSelectedAnswers((prev) => ({ ...prev, [qid]: choice }));
  };

  const handleSubmit = async () => {
    try {
      setSubmitting(true);
      const payload = questions.map((q) => ({
        question_id: q.id,
        answer: selectedAnswers[q.id] || "",
      }));

      const { score, total, results } = await submitQuizAnswers({
        answers: payload,
        domain,
      });

      setFeedback({ score, total, results });
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      console.error("Quiz submission error:", err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleRetry = () => {
    setSelectedAnswers({});
    setFeedback(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleNewQuiz = () => {
    setSelectedAnswers({});
    setFeedback(null);
    setQuestions([]);
    setStarted(false);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const allAnswered = useMemo(() => {
    if (!questions.length) return false;
    return Object.keys(selectedAnswers).length >= questions.length;
  }, [questions.length, selectedAnswers]);

  const scorePct = useMemo(() => {
    if (!feedback?.total) return 0;
    return Math.round((feedback.score / feedback.total) * 100);
  }, [feedback]);

  const scoreBadge = useMemo(() => {
    if (!feedback) return "";
    if (scorePct >= 80) return "bg-emerald-500/15 text-emerald-200 ring-1 ring-emerald-500/30";
    if (scorePct >= 50) return "bg-amber-500/15 text-amber-200 ring-1 ring-amber-500/30";
    return "bg-rose-500/15 text-rose-200 ring-1 ring-rose-500/30";
  }, [feedback, scorePct]);

  return (
    <div className="min-h-[calc(100vh-64px)] bg-slate-950">
      <div className="max-w-6xl mx-auto px-4 py-10">
        {/* header row */}
        <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-slate-400 text-sm">Quizzes</p>
            <h1 className="text-3xl md:text-4xl font-semibold text-white tracking-tight">
              Security+ Quiz Mode
            </h1>
            <p className="text-slate-400 mt-2 max-w-2xl">
              Choose a domain and number of questions. Submit to get explanations and track your progress.
            </p>
          </div>

          {started && (
            <div className="flex gap-3 mt-4 md:mt-0">
              <button
                onClick={handleNewQuiz}
                className="px-4 py-2 rounded-xl bg-white/5 text-slate-200 ring-1 ring-white/10 hover:bg-white/10 transition"
              >
                New Quiz
              </button>
            </div>
          )}
        </div>

        {/* start panel */}
        {!started ? (
          <div className="mt-10 rounded-2xl bg-white/5 ring-1 ring-white/10 p-6">
            <div className="grid gap-4 md:grid-cols-3">
              <div>
                <label className="block text-slate-200 font-medium mb-2">
                  Choose Domain
                </label>
                <select
                  className="w-full rounded-xl bg-slate-900/50 text-slate-100 ring-1 ring-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-sky-400/40"
                  value={domain}
                  onChange={(e) => setDomain(e.target.value)}
                >
                  <option>Random</option>
                  <option>Attacks</option>
                  <option>Architecture</option>
                  <option>Implementation</option>
                </select>
                <p className="text-slate-400 text-xs mt-2">
                  “Random” pulls a mix across domains.
                </p>
              </div>

              <div>
                <label className="block text-slate-200 font-medium mb-2">
                  Number of Questions
                </label>
                <input
                  type="number"
                  min="1"
                  max="50"
                  className="w-full rounded-xl bg-slate-900/50 text-slate-100 ring-1 ring-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-sky-400/40"
                  value={count}
                  onChange={(e) => setCount(+e.target.value)}
                />
              </div>

              <div className="flex items-end">
                <button
                  onClick={startQuiz}
                  disabled={starting}
                  className={`w-full px-4 py-2 rounded-xl font-semibold ring-1 transition
                    ${
                      starting
                        ? "bg-sky-500/10 text-sky-200 ring-sky-500/20 cursor-not-allowed"
                        : "bg-sky-500/15 text-sky-200 ring-sky-500/25 hover:bg-sky-500/25"
                    }`}
                >
                  {starting ? "Starting…" : "Start Quiz"}
                </button>
              </div>
            </div>
          </div>
        ) : (
          <>
            {/* results summary (only after submit) */}
            {feedback && (
              <div className="mt-8 rounded-2xl bg-white/5 ring-1 ring-white/10 p-5 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className={`px-3 py-1 rounded-full text-sm font-semibold ${scoreBadge}`}>
                    {scorePct}%
                  </div>
                  <div>
                    <p className="text-white font-semibold">
                      Score: {feedback.score}/{feedback.total}
                    </p>
                    <p className="text-slate-400 text-sm">
                      Review explanations below. Your progress was saved.
                    </p>
                  </div>
                </div>

                <div className="flex gap-3">
                  <button
                    onClick={handleRetry}
                    className="px-4 py-2 rounded-xl bg-sky-500/15 text-sky-200 ring-1 ring-sky-500/25 hover:bg-sky-500/25 transition"
                  >
                    Retry Quiz
                  </button>
                  <button
                    onClick={handleNewQuiz}
                    className="px-4 py-2 rounded-xl bg-white/5 text-slate-200 ring-1 ring-white/10 hover:bg-white/10 transition"
                  >
                    New Quiz
                  </button>
                </div>
              </div>
            )}

            {/* questions */}
            <div className="mt-8 space-y-5">
              {questions.map((q, idx) => {
                const result = feedback?.results.find((r) => r.question_id === q.id);

                return (
                  <div
                    key={q.id}
                    className={[
                      "rounded-2xl bg-white/5 ring-1 p-6",
                      result
                        ? result.correct
                          ? "ring-emerald-500/25"
                          : "ring-rose-500/25"
                        : "ring-white/10 hover:ring-white/20 transition",
                    ].join(" ")}
                  >
                    {/* question header */}
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <p className="text-slate-400 text-sm">Question {idx + 1}</p>
                        <h3 className="text-white text-lg md:text-xl font-semibold mt-1">
                          {q.question}
                        </h3>
                      </div>

                      {feedback && result && (
                        <div
                          className={[
                            "px-3 py-1 rounded-full text-sm font-semibold shrink-0",
                            result.correct
                              ? "bg-emerald-500/15 text-emerald-200 ring-1 ring-emerald-500/30"
                              : "bg-rose-500/15 text-rose-200 ring-1 ring-rose-500/30",
                          ].join(" ")}
                        >
                          {result.correct ? "Correct" : "Incorrect"}
                        </div>
                      )}
                    </div>

                    {/* options */}
                    <div className="mt-5 grid gap-2">
                      {q.choices.map((choice) => {
                        const selected = selectedAnswers[q.id] === choice;
                        const disabled = !!feedback;

                        // after feedback: tint the correct answer row, and tint the selected row if wrong
                        let state = "neutral";
                        if (feedback && result) {
                          if (choice === result.correct_answer) state = "correct";
                          else if (!result.correct && selected) state = "wrong";
                        }

                        return (
                          <OptionRow
                            key={choice}
                            label={choice}
                            selected={selected}
                            disabled={disabled}
                            state={state}
                            onClick={() => handlePick(q.id, choice)}
                          />
                        );
                      })}
                    </div>

                    {/* explanation block */}
                    {feedback && result && (
                      <div className="mt-5 rounded-xl bg-slate-900/40 ring-1 ring-white/10 p-4">
                        {!result.correct && (
                          <p className="text-slate-200 text-sm">
                            <span className="text-slate-400">Your answer:</span>{" "}
                            <span className="font-semibold">
                              {selectedAnswers[q.id] || "(none)"}
                            </span>
                            <span className="text-slate-400"> • Correct:</span>{" "}
                            <span className="font-semibold">
                              {result.correct_answer}
                            </span>
                          </p>
                        )}

                        <p className="text-slate-200 text-sm mt-2">
                          <span className="text-slate-400">Explanation:</span>{" "}
                          {result.explanation}
                        </p>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* action row */}
            <div className="mt-6 flex justify-end gap-3">
              <button
                onClick={handleNewQuiz}
                className="px-4 py-2 rounded-xl bg-white/5 text-slate-200 ring-1 ring-white/10 hover:bg-white/10 transition"
              >
                Reset
              </button>

              <button
                onClick={handleSubmit}
                disabled={!allAnswered || !!feedback || submitting}
                className={`px-5 py-2 rounded-xl font-semibold ring-1 transition
                  ${
                    !allAnswered || feedback || submitting
                      ? "bg-emerald-500/10 text-emerald-200 ring-emerald-500/20 cursor-not-allowed"
                      : "bg-emerald-500/15 text-emerald-200 ring-emerald-500/25 hover:bg-emerald-500/25"
                  }`}
              >
                {submitting ? "Submitting…" : "Submit"}
              </button>
            </div>

            <div className="mt-6 text-center text-slate-500 text-sm">
              Tip: Submit to log results to your dashboard.
            </div>
          </>
        )}
      </div>
    </div>
  );
}
