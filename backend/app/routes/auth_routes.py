from flask import Blueprint, request, jsonify
from app.models.user import User
from flask_jwt_extended import create_access_token
from app.services.auth import hash_password, check_password
from app.extensions import db
from sqlalchemy.exc import IntegrityError

#set up flask blueprint for grouping auth routes
auth_bp = Blueprint("auth", __name__, url_prefix="/api")


#POST /api/register route

@auth_bp.route("/register", methods=["POST"])
def register():
    #parse incoming JSON
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    #basic validation
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    #prevent duplicate sign-ups
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    # hash the password before saving
    hashed_pw = hash_password(password)
    new_user = User(email=email, password=hashed_pw)
    db.session.add(new_user)

    # catch any race-condition duplicates at commit time
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "User already exists"}), 400

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
    #temporarily(?) trying to make this email instead of id
    token = create_access_token(identity=user.email)


    #return token and user info to frontend

    return jsonify({
        "token": token,
        "user": user.to_dict()
    }), 200

