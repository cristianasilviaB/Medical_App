from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import model
import schemas
from router.auth import get_current_user

router = APIRouter(prefix="/patients", tags=["Patients"])


# CREATE - Protected route (JSON body validation)
@router.post(
    "/",
    response_model=schemas.PatientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    doctor = (
        db.query(model.Doctor)
        .filter(model.Doctor.id == patient.doctor_id)
        .first()
    )
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )

    db_patient = model.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


# READ ALL - Public route
@router.get("/", response_model=List[schemas.PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    return (
        db.query(model.Patient)
        .filter(model.Patient.is_deleted.is_(False))
        .all()
    )


# READ ONE - Public route
@router.get("/{patient_id}", response_model=schemas.PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = (
        db.query(model.Patient)
        .filter(
            model.Patient.id == patient_id,
            model.Patient.is_deleted.is_(False),
        )
        .first()
    )
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    return patient

# 4. UPDATE - Protected route (JSON body validation)
@router.put("/{patient_id}", response_model=schemas.PatientResponse)
def update_patient(
    patient_id: int,
    patient_update: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    db_patient = (
        db.query(model.Patient)
        .filter(
            model.Patient.id == patient_id,
            model.Patient.is_deleted.is_(False),
        )
        .first()
    )
    if not db_patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )

    doctor = (
        db.query(model.Doctor)
        .filter(model.Doctor.id == patient_update.doctor_id)
        .first()
    )
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )

    for key, value in patient_update.model_dump().items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)
    return db_patient


# SOFT DELETE - Protected route
@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    patient = (
        db.query(model.Patient)
        .filter(
            model.Patient.id == patient_id,
            model.Patient.is_deleted.is_(False),
        )
        .first()
    )
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )

    patient.is_deleted = True
    db.commit()
    return {
        "message": f"Patient with ID {patient_id} has been soft-deleted successfully"
    }