# app/models/lab.py
from app.extensions import db
from datetime import datetime

class LabScenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    log_data = db.Column(db.Text, nullable=False)  #fake logs
    question = db.Column(db.String, nullable=False)
    choices = db.Column(db.PickleType, nullable=False)  #list of strings
    answer = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "log_data": self.log_data,
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

class LabAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # foreign key later if you want
    lab_id = db.Column(db.Integer, nullable=False)
    selected_answer = db.Column(db.String, nullable=False)
    correct = db.Column(db.Boolean, nullable=False)
