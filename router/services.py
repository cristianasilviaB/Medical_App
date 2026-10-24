from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
import model
import schemas
from router.auth import get_current_user
from services.medical_service_service import MedicalServiceService

router = APIRouter(prefix="/services", tags=["Medical Services"])


# CREATE - Protected route
@router.post(
    "/",
    response_model=schemas.MedicalServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service(
    service: schemas.MedicalServiceCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    medical_service_service = MedicalServiceService(db)
    return medical_service_service.create_service(service)


# READ ALL - Public route
@router.get("/", response_model=List[schemas.MedicalServiceResponse])
def get_services(db: Session = Depends(get_db)):
    medical_service_service = MedicalServiceService(db)
    return medical_service_service.get_all_services()


# READ ONE - Public route
@router.get("/{service_id}", response_model=schemas.MedicalServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    medical_service_service = MedicalServiceService(db)
    return medical_service_service.get_service_by_id(service_id)