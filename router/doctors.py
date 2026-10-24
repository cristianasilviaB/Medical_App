from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
import model
import schemas
from router.auth import get_current_user
from services.doctor_service import DoctorService

router = APIRouter(prefix="/doctors", tags=["Doctors"])


# 1. CREATE - Protected route
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
    doctor_service = DoctorService(db)
    return doctor_service.create_doctor(doctor)


# 2. READ ALL - Public route
@router.get("/", response_model=List[schemas.DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    doctor_service = DoctorService(db)
    return doctor_service.get_all_doctors()


# 3. READ ONE - Public route
@router.get("/{doctor_id}", response_model=schemas.DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor_service = DoctorService(db)
    return doctor_service.get_doctor_by_id(doctor_id)