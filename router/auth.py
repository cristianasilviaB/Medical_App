from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import model

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    existing_user = (
        db.query(model.User).filter(model.User.username == username).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = model.User(username=username, hashed_password=password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}


@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = (
        db.query(model.User)
        .filter(
            model.User.username == username,
            model.User.hashed_password == password,
        )
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Invalid username or password"
        )
    return {"message": "Login successful", "username": username}