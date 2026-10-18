from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import model
from router.auth import get_current_user

router = APIRouter(prefix="/doctors", tags=["Doctors"])


# CREATE - Protected route (requires valid JWT token)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_doctor(
    name: str,
    specialization: str,
    phone: str,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    doctor = model.Doctor(name=name, specialization=specialization, phone=phone)
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


# READ ALL - Public route (retrieve list of all doctors)
@router.get("/")
def get_doctors(db: Session = Depends(get_db)):
    return db.query(model.Doctor).all()


# READ ONE - Public route (retrieve a specific doctor by ID)
@router.get("/{doctor_id}")
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(model.Doctor).filter(model.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )
    return doctor


#UPDATE - Protected route (requires valid JWT token)
@router.put("/{doctor_id}")
def update_doctor(
    doctor_id: int,
    name: str,
    specialization: str,
    phone: str,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    doctor = db.query(model.Doctor).filter(model.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )

    doctor.name = name
    doctor.specialization = specialization
    doctor.phone = phone
    db.commit()
    db.refresh(doctor)
    return doctor


# DELETE - Protected route (requires valid JWT token)
@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    doctor = db.query(model.Doctor).filter(model.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )

    db.delete(doctor)
    db.commit()
    return {"message": f"Doctor with ID {doctor_id} has been deleted successfully"}