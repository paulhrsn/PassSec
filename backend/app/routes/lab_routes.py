# app/routes/lab_routes.py
from flask import Blueprint, jsonify, request
from app.models.lab import LabScenario

#create new blueprint for lab-related routes
lab_bp = Blueprint("lab", __name__, url_prefix="/api")





# POST /api/lab/submit to submit an answer to a lab
@lab_bp.route("/labs/submit", methods=["POST"])
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
@lab_bp.route("/labs/<int:lab_id>", methods=["GET"])
def get_lab_by_id(lab_id: int):
    lab = LabScenario.query.get(lab_id)
    if not lab:
        return jsonify({"error": "Lab not found"}), 404
    return jsonify(lab.to_dict()), 200


@lab_bp.route("/labs", methods=["GET"])
def get_all_labs():
    labs = LabScenario.query.all()  #fetch all LabScenario rows from the database

    #convert each lab to a dict with just the fields we need for the list view
    lab_list = [{
        "id": lab.id,
        "title": lab.title
    } for lab in labs]

    return jsonify(lab_list)  #return as JSON to the frontend
