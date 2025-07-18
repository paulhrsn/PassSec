from flask import Blueprint, jsonify
from app.models.quiz import QuizQuestion

quiz_bp = Blueprint("quiz", __name__, url_prefix="/api")

@quiz_bp.route("/quiz", methods=["GET"])
def get_quiz_questions():
    questions = QuizQuestion.query.all()
    return jsonify([q.to_dict() for q in questions]), 200