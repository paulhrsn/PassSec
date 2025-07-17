# extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def init_extensions(app):
    CORS(app)
    db = SQLAlchemy()
    bcrypt = Bcrypt()
    jwt = JWTManager()
