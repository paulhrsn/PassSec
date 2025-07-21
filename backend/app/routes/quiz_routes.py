from flask import Blueprint, jsonify, request
from sqlalchemy.sql.expression import func            
from app.models.quiz import QuizQuestion

quiz_bp = Blueprint("quiz", __name__, url_prefix="/api")

@quiz_bp.route("/quiz", methods=["GET"])
def get_quiz_questions():
    # ── 1. read params with sane defaults ─────────────────────────────────────────
    try:
        count  = int(request.args.get("count", 10))
        count  = max(1, min(count, 50))          # 1-50 so nobody asks for huge amount
    except ValueError:
        count = 10

    domain = request.args.get("domain", "").strip()

    # ── 2. build the query ────────────────────────────────────────────────────────
    query = QuizQuestion.query
    if domain and domain.lower() != "random":
        query = query.filter_by(domain=domain)

    # random order, then limit
    questions = (query.order_by(func.random())   # SQLite / Postgres random ordering
                      .limit(count)
                      .all())

    return jsonify([q.to_dict() for q in questions]), 200







@quiz_bp.route("/quiz/submit", methods=["POST"])
def submit_quiz_answers():

    data = request.get_json() or {}
    answers = data.get("answers", [])

    correct = 0
    for ans in answers:
        q = QuizQuestion.query.get(ans.get("question_id"))
        if q and q.answer.strip().lower() == (ans.get("answer","").strip().lower()):
            correct += 1

    return jsonify({
        "score": correct,
        "total": len(answers)
    }), 200