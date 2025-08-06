# backend/app/routes/dashboard_routes.py

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.user_quiz_history import UserQuizHistory
from app.models.lab import LabAttempt
from app.extensions import db

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/stats", methods=["GET"])
@jwt_required()
def get_user_stats():
    # get current user
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # 1) get quiz history
    quiz_history = UserQuizHistory.query.filter_by(user_id=user.id).all()
    quiz_stats = {}
    for entry in quiz_history:
        dom = entry.domain or "Unknown"
        if dom not in quiz_stats:
            quiz_stats[dom] = {"correct": 0, "total": 0}
        quiz_stats[dom]["correct"] += entry.correct
        quiz_stats[dom]["total"]   += entry.total

    # 2) get lab attempts
    lab_history = LabAttempt.query.filter_by(user_id=user.id).all()
    lab_stats = {"Labs": {"correct": 0, "total": 0}}
    for attempt in lab_history:
        lab_stats["Labs"]["total"]   += 1
        if attempt.correct:
            lab_stats["Labs"]["correct"] += 1

    # 3) format both into a single list of { domain, correct, total, percent }
    results = []
    #quiz domains
    for domain, data in quiz_stats.items():
        c = data["correct"]
        t = data["total"]
        results.append({
            "domain": domain,
            "correct": c,
            "total": t,
            "percent": round((c / t) * 100) if t else 0
        })
    #labs bucket
    for domain, data in lab_stats.items():
        c = data["correct"]
        t = data["total"]
        results.append({
            "domain": domain,
            "correct": c,
            "total": t,
            "percent": round((c / t) * 100) if t else 0
        })

    return jsonify(results), 200
