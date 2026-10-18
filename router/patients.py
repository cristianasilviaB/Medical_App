from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import model
from router.auth import get_current_user

router = APIRouter(prefix="/patients", tags=["Patients"])


# CREATE - Protected route (requires valid JWT token)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_patient(
    name: str,
    age: int,
    disease: str,
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    doctor = db.query(model.Doctor).filter(model.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )

    patient = model.Patient(
        name=name, age=age, disease=disease, doctor_id=doctor_id
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


# READ ALL - Public route (retrieve list of all patients)
@router.get("/")
def get_patients(db: Session = Depends(get_db)):
    return db.query(model.Patient).all()


#  READ ONE - Public route (retrieve a specific patient by ID)
@router.get("/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = (
        db.query(model.Patient).filter(model.Patient.id == patient_id).first()
    )
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    return patient


# UPDATE - Protected route (requires valid JWT token)
@router.put("/{patient_id}")
def update_patient(
    patient_id: int,
    name: str,
    age: int,
    disease: str,
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    patient = (
        db.query(model.Patient).filter(model.Patient.id == patient_id).first()
    )
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )

    doctor = db.query(model.Doctor).filter(model.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )

    patient.name = name
    patient.age = age
    patient.disease = disease
    patient.doctor_id = doctor_id
    db.commit()
    db.refresh(patient)
    return patient


#  DELETE - Protected route (requires valid JWT token)
@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    patient = (
        db.query(model.Patient).filter(model.Patient.id == patient_id).first()
    )
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )

    db.delete(patient)
    db.commit()
    return {"message": f"Patient with ID {patient_id} has been deleted successfully"}