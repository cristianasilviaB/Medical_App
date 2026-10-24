from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.service_repository import ServiceRepository
import model
import schemas


class MedicalServiceService:
    def __init__(self, db: Session):
        self.service_repo = ServiceRepository(db)

    def get_all_services(self) -> List[model.MedicalService]:
        # Retrieve all medical services via repository
        return self.service_repo.get_all()

    def get_service_by_id(self, service_id: int) -> model.MedicalService:
        # Retrieve medical service by ID or raise HTTP 404
        service = self.service_repo.get_by_id(service_id)
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical service not found",
            )
        return service

    def create_service(self, service_schema: schemas.MedicalServiceCreate) -> model.MedicalService:
        # Create a new medical service record via repository
        return self.service_repo.create(service_schema)