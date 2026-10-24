from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
import model
import schemas
from router.auth import get_current_user
from services.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["Patients"])


# CREATE - Protected route
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
    patient_service = PatientService(db)
    return patient_service.create_patient(patient)

#  READ ALL - Public route
@router.get("/", response_model=List[schemas.PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    patient_service = PatientService(db)
    return patient_service.get_all_patients()

#  READ ONE - Public route
@router.get("/{patient_id}", response_model=schemas.PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient_service = PatientService(db)
    return patient_service.get_patient_by_id(patient_id)

# UPDATE - Protected route
@router.put("/{patient_id}", response_model=schemas.PatientResponse)
def update_patient(
    patient_id: int,
    patient_update: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    patient_service = PatientService(db)
    return patient_service.update_patient(patient_id, patient_update)

# SOFT DELETE - Protected route
@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    patient_service = PatientService(db)
    patient_service.soft_delete_patient(patient_id)
    return {
        "message": f"Patient with ID {patient_id} has been soft-deleted successfully"
    }