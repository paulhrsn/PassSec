# backend/app/routes/quiz_routes.py

from flask import Blueprint, jsonify, request
from sqlalchemy.sql.expression import func
from app.models.quiz import QuizQuestion

#create a Blueprint for all /api/quiz routes
quiz_bp = Blueprint("quiz", __name__)


@quiz_bp.route("/quiz", methods=["GET"])
def get_quiz_questions():

    try:
        count = int(request.args.get("count", 10))
    except ValueError:
        count = 10
    count = max(1, min(count, 50))

    domain = request.args.get("domain", "").strip()

    query = QuizQuestion.query
    if domain and domain.lower() != "random":
        # assumes your QuizQuestion model has a `domain` column
        query = query.filter_by(domain=domain)

    questions = (
        query
        .order_by(func.random())  # random ordering (works in SQLite/Postgres)
        .limit(count)
        .all()
    )

    return jsonify([q.to_dict() for q in questions]), 200


@quiz_bp.route("/quiz/submit", methods=["POST"])
def submit_quiz_answers():

    data = request.get_json(silent=True) or {}
    answers = data.get("answers", [])

    results = []
    correct_count = 0

    for ans in answers:
        qid      = ans.get("question_id")
        user_ans = (ans.get("answer") or "").strip().lower()
        question = QuizQuestion.query.get(qid)

        if not question:
            # skip or mark as wrong
            continue

        is_correct = (question.answer.strip().lower() == user_ans)
        if is_correct:
            correct_count += 1

        results.append({
            "question_id":    qid,
            "correct":        is_correct,
            "correct_answer": question.answer,
            "explanation":    question.explanation  
        })

    return jsonify({
        "score":  correct_count,
        "total":  len(results),
        "results": results
    }), 200

