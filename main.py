from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database, auth

app = FastAPI()

# Créer toutes les tables dans la base de données
database.Base.metadata.create_all(bind=database.engine)

# Dépendance pour obtenir une session de base de données
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = auth.hash_password(password)
    db_user = models.User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"username": db_user.username}

@app.post("/login/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not auth.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"message": "Login successful"}