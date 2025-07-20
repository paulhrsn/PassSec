# app/routes/lab_routes.py
from flask import Blueprint, jsonify, request
from app.models.lab import LabScenario

#create new blueprint for lab-related routes
lab_bp = Blueprint("lab", __name__, url_prefix="/api")


# GET /api/lab to fetch all the lab scenarios
@lab_bp.route("/lab", methods=["GET"])
def get_labs():
    #query all lab entries from the database
    labs = LabScenario.query.all()
    
    #convert each lab to a dictionary and return as JSON
    return jsonify([lab.to_dict() for lab in labs]), 200


# POST /api/lab/submit to submit an answer to a lab
@lab_bp.route("/lab/submit", methods=["POST"])
def submit_lab_answer():
    #parse the JSON body of the request
    data = request.get_json()
    lab_id = data.get("lab_id")          #id of the lab scenario
    user_answer = data.get("answer")     # sswer submitted by user

    #try to find the lab scenario in the DB
    lab = LabScenario.query.get(lab_id)
    if not lab:
        return jsonify({"error": "Lab not found"}), 404

    #compare user answer to correct answer (case-insensitive)
    correct = lab.answer.strip().lower() == user_answer.strip().lower()

    #return whether answer was correct, and what the correct answer is
    return jsonify({
        "correct": correct,
        "correct_answer": lab.answer
    }), 200

# GET /api/lab/<lab_id> to fetch a single lab by ID
@lab_bp.route("/lab/<string:lab_id>", methods=["GET"])
def get_lab_by_id(lab_id):
    lab = LabScenario.query.get(lab_id)
    if not lab:
        return jsonify({"error": "Lab not found"}), 404
    return jsonify(lab.to_dict()), 200
