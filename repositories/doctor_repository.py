from typing import List, Optional
from sqlalchemy.orm import Session
import model
import schemas


class DoctorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[model.Doctor]:
        # Fetch all doctors from the database
        return self.db.query(model.Doctor).all()

    def get_by_id(self, doctor_id: int) -> Optional[model.Doctor]:
        # Fetch a single doctor by ID
        return (
            self.db.query(model.Doctor)
            .filter(model.Doctor.id == doctor_id)
            .first()
        )

    def create(self, doctor: schemas.DoctorCreate) -> model.Doctor:
        # Create and persist a new doctor record
        db_doctor = model.Doctor(**doctor.model_dump())
        self.db.add(db_doctor)
        self.db.commit()
        self.db.refresh(db_doctor)
        return db_doctor