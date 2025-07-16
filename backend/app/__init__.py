
from flask import Flask
from config import Config
from .routes import register_routes
from db import db
def create_app():
    #factory to create/configure flask app, building app in a function to make modularity easier
    app = Flask(__name__)
    app.config.from_object(Config) #load our config class
    db.init_app(app) #bind sqlachlemy to this app 
    register_routes(app) #register all blueprints
    return app