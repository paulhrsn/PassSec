from flask import Blueprint, request, jsonify
from app.models.user import User
from app.services.auth import check_password
from flask_jwt_extended import create_access_token

#set up flask blueprint for grouping auth routes
auth_bp = Blueprint("auth", __name__, url_prefix="/api")

#POST /api/login route
@auth_bp.route("/login", methods=["POST"])
def login():
    #get json from frontend, expecting {email, password}
    data = request.get_json()

    #validate input fields exist
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password required"}), 400
    
    email = data["email"]
    password = data["password"]

    #look for user in database
    user = User.query.filter_by(email=email).first()

    #if no user/wrong password return an error
    if not user or not check_password(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    #If it is valid create a JWT token where user.id becomes the identity
    token = create_access_token(identity=user.id)

    #return token and user info to frontend

    return jsonify({
        "token": token,
        "user": user.to_dict()
    })