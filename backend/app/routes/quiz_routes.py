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
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.user_quiz_history import UserQuizHistory
from app.extensions import db

@quiz_bp.route("/quiz/submit", methods=["POST"])
@jwt_required()  
def submit_quiz_answers():
    #get email from jwt
    user_email = get_jwt_identity()

    #look up the user
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({"error": "user not found"}), 404

    #parse json body
    data = request.get_json(silent=True) or {}

    #list of { question_id, answer }
    answers = data.get("answers", [])

    #will hold per-question feedback for the frontend
    results = []
    correct_count = 0

    #loop over each submitted answer
    for ans in answers:
        qid = ans.get("question_id")
        user_ans = (ans.get("answer") or "").strip().lower()

        # oad the question so we can compare and get its domain
        question = QuizQuestion.query.get(qid)
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
