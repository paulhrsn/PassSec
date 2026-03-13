from app.extensions import bcrypt
import re


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


#hash plain-text pw to store

def hash_password(plain_text):
    #bcrypt returns bytes, decode to string
    return bcrypt.generate_password_hash(plain_text).decode('utf-8')


#check if a plain-text pw matches stored hash
def check_password (hashed, plain_text):
    return bcrypt.check_password_hash(hashed, plain_text)


def normalize_email(value: str | None) -> str:
    return (value or "").strip().lower()


def is_valid_email(value: str) -> bool:
    return bool(EMAIL_RE.match(value))


def validate_password(password: str | None) -> tuple[bool, str]:
    raw = password or ""
    if len(raw) < 10:
        return False, "Password must be at least 10 characters."
    if len(raw) > 128:
        return False, "Password cannot exceed 128 characters."
    return True, ""