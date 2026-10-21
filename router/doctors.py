from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import model
import schemas
from router.auth import get_current_user

router = APIRouter(prefix="/doctors", tags=["Doctors"])


# 1. CREATE - Protected route (JSON body validation)
@router.post(
    "/",
    response_model=schemas.DoctorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_doctor(
    doctor: schemas.DoctorCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    db_doctor = model.Doctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


# 2. READ ALL - Public route
@router.get("/", response_model=List[schemas.DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    return db.query(model.Doctor).all()


# 3. READ ONE - Public route
@router.get("/{doctor_id}", response_model=schemas.DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = (
        db.query(model.Doctor).filter(model.Doctor.id == doctor_id).first()
    )
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )
    return doctor


# 4. UPDATE - Protected route (JSON body validation)
@router.put("/{doctor_id}", response_model=schemas.DoctorResponse)
def update_doctor(
    doctor_id: int,
    doctor_update: schemas.DoctorCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    db_doctor = (
        db.query(model.Doctor).filter(model.Doctor.id == doctor_id).first()
    )
    if not db_doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )

    for key, value in doctor_update.model_dump().items():
        setattr(db_doctor, key, value)

    db.commit()
    db.refresh(db_doctor)
    return db_doctor


# 5. DELETE - Protected route
@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    doctor = (
        db.query(model.Doctor).filter(model.Doctor.id == doctor_id).first()
    )
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )

    db.delete(doctor)
    db.commit()
    return {
        "message": f"Doctor with ID {doctor_id} has been deleted successfully"
    }