# app/models/quiz.py
from app.extensions import db

class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(100), nullable=False)  #like "threats" or "architecture"
    question = db.Column(db.Text, nullable=False) #question prompt.
    choices = db.Column(db.JSON, nullable=False)  # list of answer choices as JSON for safe serialization
    answer = db.Column(db.String, nullable=False)#the correct answer choice, index 0-3
    explanation = db.Column(db.Text, nullable=False)   #explanation


    def to_dict(self):
        return {
            "id": self.id,
            "domain": self.domain,
            "question": self.question,
            "choices": self.choices,
            "explanation": "",
        }

