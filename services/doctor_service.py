from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.doctor_repository import DoctorRepository
import model
import schemas


class DoctorService:
    def __init__(self, db: Session):
        self.doctor_repo = DoctorRepository(db)

    def get_all_doctors(self) -> List[model.Doctor]:
        # Retrieve all doctors via repository
        return self.doctor_repo.get_all()

    def get_doctor_by_id(self, doctor_id: int) -> model.Doctor:
        # Retrieve doctor by ID or raise HTTP 404
        doctor = self.doctor_repo.get_by_id(doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found",
            )
        return doctor

    def create_doctor(self, doctor_schema: schemas.DoctorCreate) -> model.Doctor:
        # Create a new doctor record via repository
        return self.doctor_repo.create(doctor_schema)