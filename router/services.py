from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import model
import schemas
from router.auth import get_current_user

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
    db_service = model.MedicalService(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


# READ ALL - Public route
@router.get("/", response_model=List[schemas.MedicalServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return db.query(model.MedicalService).all()


# READ ONE - Public route
@router.get("/{service_id}", response_model=schemas.MedicalServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = (
        db.query(model.MedicalService)
        .filter(model.MedicalService.id == service_id)
        .first()
    )
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Medical service not found"
        )
    return service