# backend/app/__init__.py

import os
from flask import Flask
from dotenv import load_dotenv

#load variables from .env so things like secret keys and database url are ready to use
load_dotenv(override=True)

from app.config import Config           
from app.extensions import init_extensions 
from app.cli import create_user            


def create_app() -> Flask:
  
    app = Flask(__name__)

    # load all the settings from our config class
    app.config.from_object(Config)

    # quick printouts to make sure it’s loading the right stuff (safe values only)
    print("→ db uri:", app.config.get("SQLALCHEMY_DATABASE_URI"))
    print("→ jwt key set:", bool(app.config.get("JWT_SECRET_KEY")))
    print("→ cors origins:", app.config.get("CORS_ORIGINS", "not set"))

    init_extensions(app)

    from app.routes.auth_routes import auth_bp
    from app.routes.health import health_bp
    from app.routes.quiz_routes import quiz_bp
    from app.routes.lab_routes import lab_bp
    from app.routes.dashboard_routes import dashboard_bp

    # mount the routes under /api so the frontend paths don’t get messy
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(quiz_bp, url_prefix="/api")
    app.register_blueprint(lab_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/api")

    # add our custom terminal commands like "flask create-user"
    app.cli.add_command(create_user)

    @app.errorhandler(401)
    def _unauthorized(err):
        return {"error": "unauthorized"}, 401

    @app.errorhandler(404)
    def _not_found(err):
        return {"error": "not found"}, 404

    return app
