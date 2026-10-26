from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
import model
import schemas
from router.auth import get_current_user
from services.appointment_service import AppointmentService

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
    appointment_service = AppointmentService(db)
    return appointment_service.create_appointment(appointment)


# READ ALL - Public route
@router.get("/", response_model=List[schemas.AppointmentResponse])
def get_appointments(db: Session = Depends(get_db)):
    appointment_service = AppointmentService(db)
    return appointment_service.get_all_appointments()


# READ ONE - Public route
@router.get("/{appointment_id}", response_model=schemas.AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment_service = AppointmentService(db)
    return appointment_service.get_appointment_by_id(appointment_id)


# 4. UPDATE STATUS - Protected route
@router.patch("/{appointment_id}/status", response_model=schemas.AppointmentResponse)
def update_appointment_status(
    appointment_id: int,
    status_update: schemas.AppointmentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    appointment_service = AppointmentService(db)
    return appointment_service.update_appointment_status(appointment_id, status_update)


# DELETE - Protected route
@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    appointment_service = AppointmentService(db)
    appointment_service.delete_appointment(appointment_id)
    return {
        "message": f"Appointment with ID {appointment_id} has been deleted successfully"
    }