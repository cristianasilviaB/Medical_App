from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import model

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("/")
def create_patient(
    name: str,
    age: int,
    disease: str,
    doctor_id: int,
    db: Session = Depends(get_db),
):
    doctor = (
        db.query(model.Doctor).filter(model.Doctor.id == doctor_id).first()
    )
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    patient = model.Patient(
        name=name, age=age, disease=disease, doctor_id=doctor_id
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("/")
def get_patients(db: Session = Depends(get_db)):
    return db.query(model.Patient).all()