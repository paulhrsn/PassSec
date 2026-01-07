# backend/app/routes/dashboard_routes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.user_quiz_history import UserQuizHistory
from app.extensions import db

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/stats", methods=["GET"])
@jwt_required()
def get_user_stats():
    ident = get_jwt_identity()
    user = User.query.filter_by(email=ident).first()  # we standardized on email
    if not user:
        return jsonify({"error": "User not found"}), 404

    #aggregate quizzes by domain
    totals = {}  # { domain: {correct:int, total:int} }
    for e in UserQuizHistory.query.filter_by(user_id=user.id).all():
        dom = e.domain or "Unknown"
        totals.setdefault(dom, {"correct": 0, "total": 0})
        totals[dom]["correct"] += e.correct
        totals[dom]["total"]   += e.total

    #format for frontend
    results = []
    for domain, data in totals.items():
        c, t = data["correct"], data["total"]
        results.append({
            "domain": domain,
            "correct": c,
            "total": t,
            "percent": round((c / t) * 100) if t else 0
        })

    #sort weakest to strongest 
    results.sort(key=lambda x: x["percent"])
    return jsonify(results), 200
