# seed/seed_quiz_data.py
import json
from app import create_app
from app.extensions import db
from app.models.quiz import QuizQuestion

app = create_app()

def seed_quiz_questions():
    with app.app_context():
        with open("seed/quiz_data.json") as f:
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
