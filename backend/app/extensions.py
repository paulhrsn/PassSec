# extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# create extensions so i can import them later
db     = SQLAlchemy()
bcrypt = Bcrypt()
jwt    = JWTManager()
cors = CORS()

def init_extensions(app):
    cors.init_app(
        app,
        resources={r"/api/.*": {"origins": "http://localhost:5173"}},  # Vite dev server
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )

    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)