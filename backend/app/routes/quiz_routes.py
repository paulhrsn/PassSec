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
@jwt_required()#to require valid jwt token in header
def submit_quiz_answers():
    #get the email from the JWT identity (set during login)
    user_email = get_jwt_identity()

    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    #parse the JSON body of the POST request
    data = request.get_json(silent=True) or {}

    #extract submitted answers from frontend
    answers = data.get("answers", [])

    domain = data.get("domain", "Unknown").strip() or "Unknown"

    #initialize variables to build result report and count correct answers
    results = []
    correct_count = 0

    #process each submitted answer
    for ans in answers:
        qid = ans.get("question_id")  # ID of the question being answered
        user_ans = (ans.get("answer") or "").strip().lower()  # User's selected answer (case-insensitive)

        # Look up the original question from the database
        question = QuizQuestion.query.get(qid)

        if not question:
            # If question not found (invalid ID), skip it
            continue

        # Compare user answer to correct answer (case-insensitive match)
        is_correct = (question.answer.strip().lower() == user_ans)
        if is_correct:
            correct_count += 1  # Count this as a correct answer

        # Append detailed result for this question
        results.append({
            "question_id": qid,
            "correct": is_correct,
            "correct_answer": question.answer,
            "explanation": question.explanation
        })

    # Create a new record in UserQuizHistory to store this quiz attempt
    history = UserQuizHistory(
        user_id=user.id,      # Link to the user who submitted the quiz
        domain=domain,        # Security+ domain name (e.g., "Threats")
        correct=correct_count,  # How many they got right
        total=len(results)      # How many questions they answered
    )

    # Save the new history record to the database
    db.session.add(history)
    db.session.commit()

    # Return score summary and individual question feedback to the frontend
    return jsonify({
        "score": correct_count,
        "total": len(results),
        "results": results
    }), 200

