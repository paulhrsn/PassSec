from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from dotenv import load_dotenv

#load valiues from .env file like JWT_SECRET_KEY
load_dotenv()

#create global extensions to later init
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    #config values; just for dev and prod

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret")  #remember to replace for prod

    #init extensions w/ app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)

    #register route blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    
    #cli option: create-user --email EMAIL --passwoerd PASSWORD
    @app.cli.command("create-user")
    @click.option("--email", prompt="True")
    return app