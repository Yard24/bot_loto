import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
def user_exists(email: str, db: Session) -> bool:
    return db.query(User).filter(User.email == email).first() is not None
