from typing import List, Optional
from sqlalchemy.orm import Session
import model
import schemas


class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[model.Appointment]:
        # Fetch all appointments from the database
        return self.db.query(model.Appointment).all()

    def get_by_id(self, appointment_id: int) -> Optional[model.Appointment]:
        # Fetch a single appointment by ID
        return (
            self.db.query(model.Appointment)
            .filter(model.Appointment.id == appointment_id)
            .first()
        )

    def get_by_doctor_id(self, doctor_id: int) -> List[model.Appointment]:
        # Fetch all appointments for a specific doctor
        return (
            self.db.query(model.Appointment)
            .filter(model.Appointment.doctor_id == doctor_id)
            .all()
        )

    def create(self, appointment: schemas.AppointmentCreate) -> model.Appointment:
        # Create and persist a new appointment record
        db_appointment = model.Appointment(**appointment.model_dump())
        self.db.add(db_appointment)
        self.db.commit()
        self.db.refresh(db_appointment)
        return db_appointment
  
    def update_status(self, appointment: model.Appointment, status: str) -> model.Appointment:
        # Update and persist appointment status
        appointment.status = status
        self.db.commit()
        self.db.refresh(appointment)
        return appointment

    def delete(self, appointment: model.Appointment) -> None:
        # Permanently delete an appointment record
        self.db.delete(appointment)
        self.db.commit()     