from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
import model
import schemas
from router.auth import get_current_user
from services.schedule_service import ScheduleService

router = APIRouter(prefix="/schedules", tags=["Doctor Schedules"])


@router.post(
    "/doctor/{doctor_id}",
    response_model=schemas.DoctorScheduleResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_doctor_schedule(
    doctor_id: int,
    schedule: schemas.DoctorScheduleCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    service = ScheduleService(db)
    return service.add_schedule(doctor_id, schedule)


@router.get("/doctor/{doctor_id}", response_model=List[schemas.DoctorScheduleResponse])
def get_doctor_schedules(doctor_id: int, db: Session = Depends(get_db)):
    service = ScheduleService(db)
    return service.get_doctor_schedules(doctor_id)


@router.delete("/{schedule_id}")
def delete_doctor_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    service = ScheduleService(db)
    service.delete_schedule(schedule_id)
    return {"message": f"Schedule with ID {schedule_id} has been deleted successfully"}