# app/cli.py
import click
from flask import current_app
from flask.cli import with_appcontext

@click.command("create-user")
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@with_appcontext
def create_user(email, password):
    from app import db
    from app.models.user import User
    from app.services.auth import hash_password

    if User.query.filter_by(email=email).first():
        print("❌ User already exists ❌")
        return

    hashed_pw = hash_password(password)
    user = User(email=email, password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    print(f"✅ Created user: {email}")
