from app.extensions import bcrypt

#hash plain-text pw to store

def hash_password(plain_text):
    #bcrypt returns bytes, decode to string
    return bcrypt.generate_password_hash(plain_text).decode('utf-8')

#check if a plain-text pw matches stored hash
def check_password (hashed, plain_text):
    return bcrypt.check_password_hash(hashed, plain_text)