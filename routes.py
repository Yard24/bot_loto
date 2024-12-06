from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from .models import User
from .services import hash_password

router = APIRouter()

@router.post("/users/")
def create_user(email: str, password: str):
    db: Session = SessionLocal()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=email, hashed_password=hash_password(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}
