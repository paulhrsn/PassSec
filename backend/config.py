from pathlib import Path
from dotenv import load_dotenv
import os

#load vars from a .env file next to thi script
load_dotenv(Path(__file__).parent / '.env')

class Config:
    #secret key for session cookies/json web tokens
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    #database uri that defaults to a local sqlite file
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    #turn off event notifs
    SQLALCHEMY_TRACK_MODIFICATIONS = False