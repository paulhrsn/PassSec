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
    origins = app.config.get("CORS_ORIGINS", ["http://localhost:5173"])
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": origins}},
        supports_credentials=app.config.get("CORS_SUPPORTS_CREDENTIALS", False),
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @jwt.unauthorized_loader
    def _missing_token(reason):
        return {"error": "missing or invalid token"}, 401

    @jwt.invalid_token_loader
    def _invalid_token(reason):
        return {"error": "missing or invalid token"}, 401

    @jwt.expired_token_loader
    def _expired_token(jwt_header, jwt_payload):
        return {"error": "token expired"}, 401