# seed/seed_quiz_data.py
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) # backend to python path so these imports work
from app import create_app
from app.extensions import db
from app.models.quiz import QuizQuestion

app = create_app()

def seed_quiz_questions():
    with app.app_context():
        #construct full path to the json
        json_path = os.path.join(os.path.dirname(__file__), "quiz_data.json")
        with open(json_path) as f:
            data = json.load(f)
            for item in data:
                question = QuizQuestion(
                    domain=item["domain"],
                    question=item["question"],
                    choices=item["choices"],
                    answer=item["answer"]
                )
                db.session.add(question)
            db.session.commit()
            print(f"Seeded {len(data)} quiz questions.")

if __name__ == "__main__":
    seed_quiz_questions()
