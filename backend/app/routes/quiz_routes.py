# backend/app/routes/quiz_routes.py

from flask import Blueprint, jsonify, request
from sqlalchemy.sql.expression import func
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.quiz import QuizQuestion
from app.models.user import User
from app.models.user_quiz_history import UserQuizHistory
from app.extensions import db


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


@quiz_bp.route("/quiz/domains", methods=["GET"])
def get_quiz_domains():
    domains = (
        db.session.query(QuizQuestion.domain)
        .distinct()
        .order_by(QuizQuestion.domain.asc())
        .all()
    )
    items = [d[0] for d in domains if d[0]]
    return jsonify({"domains": items}), 200

@quiz_bp.route("/quiz/submit", methods=["POST"])
@jwt_required()  
def submit_quiz_answers():
    identity = get_jwt_identity()

    user = db.session.get(User, int(identity))
    if not user:
        return jsonify({"error": "User not found"}), 404

    #parse json body
    data = request.get_json(silent=True) or {}

    #list of { question_id, answer }
    answers = data.get("answers", [])
    if not isinstance(answers, list):
        return jsonify({"error": "answers must be a list"}), 400
    if len(answers) == 0:
        return jsonify({"error": "answers cannot be empty"}), 400
    if len(answers) > 100:
        return jsonify({"error": "answers cannot exceed 100 items"}), 400

    #will hold per-question feedback for the frontend
    results = []
    correct_count = 0

    #loop over each submitted answer
    for ans in answers:
        if not isinstance(ans, dict):
            continue
        qid = ans.get("question_id")
        user_ans = (ans.get("answer") or "").strip().lower()
        if not qid:
            continue

        # oad the question so we can compare and get its domain
        question = db.session.get(QuizQuestion, qid)
        if not question:
            continue  #skip if the id is bad

        is_correct = question.answer.strip().lower() == user_ans
        if is_correct:
            correct_count += 1

        #append feedback for this question
        results.append({
            "question_id": qid,
            "correct": is_correct,
            "correct_answer": question.answer,
            "explanation": question.explanation
        })

        #create one history row per question, using the real domain
        db.session.add(
            UserQuizHistory(
                user_id=user.id,
                domain=question.domain,
                correct=1 if is_correct else 0,
                total=1
            )
        )

    #commit all rows at once
    db.session.commit()

    #send summary + per-question results back to the ui
    return jsonify({
        "score": correct_count,
        "total": len(results),
        "results": results
    }), 200
