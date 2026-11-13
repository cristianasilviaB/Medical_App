from typing import List, Optional
from sqlalchemy.orm import Session
import model
import schemas


class PatientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_active(self, skip: int = 0, limit: int = 100) -> List[model.Patient]:
        # Fetch active patients with pagination support
        return (
            self.db.query(model.Patient)
            .filter(model.Patient.is_deleted.is_(False))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, patient_id: int) -> Optional[model.Patient]:
        # Fetch an active patient by ID
        return (
            self.db.query(model.Patient)
            .filter(
                model.Patient.id == patient_id,
                model.Patient.is_deleted.is_(False),
            )
            .first()
        )

    def get_existing_patient(self, name: str, age: int) -> Optional[model.Patient]:
        # Check if an active patient with the same name and age already exists
        return (
            self.db.query(model.Patient)
            .filter(
                model.Patient.name.ilike(name.strip()),
                model.Patient.age == age,
                model.Patient.is_deleted.is_(False),
            )
            .first()
        )
        
    def create(self, patient: schemas.PatientCreate) -> model.Patient:
        # Create a new patient record
        db_patient = model.Patient(**patient.model_dump())
        self.db.add(db_patient)
        self.db.commit()
        self.db.refresh(db_patient)
        return db_patient

    def update(
        self, db_patient: model.Patient, patient_update: schemas.PatientCreate
    ) -> model.Patient:
        # Update existing patient fields
        for key, value in patient_update.model_dump().items():
            setattr(db_patient, key, value)
        self.db.commit()
        self.db.refresh(db_patient)
        return db_patient

    def soft_delete(self, patient: model.Patient) -> None:
        # Mark patient record as deleted
        patient.is_deleted = True
        self.db.commit()