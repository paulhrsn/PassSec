from flask import Flask
import os
from dotenv import load_dotenv
from app.extensions import init_extensions


#load valiues from .env file like JWT_SECRET_KEY
load_dotenv()


def create_app():
    app = Flask(__name__)
    #init extensions
    #config values; just for dev and prod

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret")  #remember to replace for prod

    init_extensions(app)

    #register route blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix = "/api")
    from app.routes.health import health_bp
    app.register_blueprint(health_bp, url_prefix="/api")
    from app.routes.quiz_routes import quiz_bp
    app.register_blueprint(quiz_bp, url_prefix="/api")
    



    # from app.routes.lab_routes import lab_bp
    # app.register_blueprint(lab_bp)
    from app import models
    from app.models import user 
    from app.cli import create_user 
    app.cli.add_command(create_user)
    return app


    