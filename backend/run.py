from app import create_app
from db import db

app = create_app() #creates flask app w/ config, routes, DB

@app.before_first_request #creates tables if they dont exist yet
def create_tables():
    #auto-create tables from models before first request
    db.create_all()