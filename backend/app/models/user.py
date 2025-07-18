from app.extensions import db
#user model as a row in the db

class User(db.Model):
    #unique id for user as primaey key
    id = db.Column(db.Integer, primary_key = True)

    #email address, has to be unique and not null
    email = db.Column(db.String(120), unique=True, nullable=False)

    #hashed pw (remember not to keep as plaintext)
    password = db.Column(db.String(200), nullable = False)

    #helper to return safe and serializable user info
    def to_dict(self):
        return{
            "id": self.id,
            "email": self.email
        }