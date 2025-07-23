# app/models/user_quiz_history.py

from datetime import datetime
from app.extensions import db

class UserQuizHistory(db.Model):
    __tablename__ = "user_quiz_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )
    domain = db.Column(db.String(100), nullable=False)
    correct = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    #relationship back to User. So from a userquizhistory u can access with .user and from a user u can access the quiz attempts via .quiz_history
    user = db.relationship("User", backref=db.backref("quiz_history", lazy="dynamic"))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "domain": self.domain,
            "correct": self.correct,
            "total": self.total,
            "timestamp": self.timestamp.isoformat(),
        }
