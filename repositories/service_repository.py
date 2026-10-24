from typing import List, Optional
from sqlalchemy.orm import Session
import model
import schemas


class ServiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[model.MedicalService]:
        # Fetch all medical services from the database
        return self.db.query(model.MedicalService).all()

    def get_by_id(self, service_id: int) -> Optional[model.MedicalService]:
        # Fetch a single medical service by ID
        return (
            self.db.query(model.MedicalService)
            .filter(model.MedicalService.id == service_id)
            .first()
        )

    def create(self, service: schemas.MedicalServiceCreate) -> model.MedicalService:
        # Create and persist a new medical service record
        db_service = model.MedicalService(**service.model_dump())
        self.db.add(db_service)
        self.db.commit()
        self.db.refresh(db_service)
        return db_service