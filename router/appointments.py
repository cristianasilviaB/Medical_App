from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import model
import schemas
from router.auth import get_current_user

router = APIRouter(prefix="/appointments", tags=["Appointments"])


# CREATE - Protected route
@router.post(
    "/",
    response_model=schemas.AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    # Verify if patient exists and is active (not soft-deleted)
    patient = (
        db.query(model.Patient)
        .filter(
            model.Patient.id == appointment.patient_id,
            model.Patient.is_deleted.is_(False),
        )
        .first()
    )
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )

    # Verify if doctor exists
    doctor = (
        db.query(model.Doctor)
        .filter(model.Doctor.id == appointment.doctor_id)
        .first()
    )
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )

    # Verify if medical service exists
    service = (
        db.query(model.MedicalService)
        .filter(model.MedicalService.id == appointment.service_id)
        .first()
    )
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Medical service not found"
        )

    db_appointment = model.Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


# READ ALL - Public route
@router.get("/", response_model=List[schemas.AppointmentResponse])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(model.Appointment).all()


# READ ONE - Public route
@router.get("/{appointment_id}", response_model=schemas.AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = (
        db.query(model.Appointment)
        .filter(model.Appointment.id == appointment_id)
        .first()
    )
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
        )
    return appointment


# DELETE - Protected route
@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    appointment = (
        db.query(model.Appointment)
        .filter(model.Appointment.id == appointment_id)
        .first()
    )
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
        )

    db.delete(appointment)
    db.commit()
    return {
        "message": f"Appointment with ID {appointment_id} has been deleted successfully"
    }