from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import model

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("/")
def create_doctor(
    name: str, specialization: str, phone: str, db: Session = Depends(get_db)
):
    doctor = model.Doctor(
        name=name, specialization=specialization, phone=phone
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.get("/")
def get_doctors(db: Session = Depends(get_db)):
    return db.query(model.Doctor).all()