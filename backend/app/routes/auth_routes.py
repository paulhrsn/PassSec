from flask import Blueprint, request, jsonify
from app.models.user import User
from flask_jwt_extended import create_access_token
from app.services.auth import hash_password, check_password
from app.extensions import db

#set up flask blueprint for grouping auth routes
auth_bp = Blueprint("auth", __name__, url_prefix="/api")


#POST /api/register route

@auth_bp.route("/register", methods=["POST"])
def register():
    #get json from frontend, expecting {email, password}
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    #check if already exists
    if User.query.filter_by(email=email).first():
        return jsonify ({"message": "User already exists"}), 400
    
    hashed_pw = hash_password(password)
    new_user = User(email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


#POST /api/login route
@auth_bp.route("/login", methods=["POST"])
def login():
    #get json from frontend, expecting {email, password}
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    #validate input fields exist
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400


    #look for user in database
    user = User.query.filter_by(email=email).first()

    #if no user/wrong password return an error
    if not user or not check_password(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    #ff it is valid create a JWT token where user.id becomes the identity
    token = create_access_token(identity=user.id)


    #return token and user info to frontend

    return jsonify({
        "token": token,
        "user": user.to_dict()
    }), 200

