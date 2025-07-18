# app/models/quiz.py
from app.extensions import db

class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(100), nullable=False)  #like "threats" or "architecture"
    question = db.Column(db.Text, nullable=False)
    choices = db.Column(db.PickleType, nullable=False)  #list of strings, using PickleType to store as byte-string python object directly in db
    answer = db.Column(db.String, nullable=False)       #the correct answer choice
