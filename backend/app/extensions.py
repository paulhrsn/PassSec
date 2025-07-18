# extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# create extensions so i can import them later
db     = SQLAlchemy()
bcrypt = Bcrypt()
jwt    = JWTManager()
cors   = CORS()

def init_extensions(app):
    CORS(app)
    #wire extensions into app
    cors.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)