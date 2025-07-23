
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.user_quiz_history import UserQuizHistory

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/stats", methods=["GET"])
@jwt_required()
def get_user_stats():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    #query all quiz attempts for this user
    history = UserQuizHistory.query.filter_by(user_id=user.id).all()

    #aggregate results for each domain
    stats = {}
    for entry in history:
        dom = entry.domain
        if dom not in stats:
            stats[dom] = {"correct": 0, "total": 0}
        stats[dom]["correct"] += entry.correct
        stats[dom]["total"] += entry.total

    #convert to list of { domain, correct, total, percent }
    formatted = []
    for domain, data in stats.items():
        total = data["total"]
        correct = data["correct"]
        formatted.append({
            "domain": domain,
            "correct": correct,
            "total": total,
            "percent": round((correct / total) * 100) if total else 0
        })

    return jsonify(formatted), 200
