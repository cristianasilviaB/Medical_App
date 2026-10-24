from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.appointment_repository import AppointmentRepository
from repositories.doctor_repository import DoctorRepository
from repositories.patient_repository import PatientRepository
from repositories.service_repository import ServiceRepository
import model
import schemas


class AppointmentService:
    def __init__(self, db: Session):
        self.appointment_repo = AppointmentRepository(db)
        self.patient_repo = PatientRepository(db)
        self.doctor_repo = DoctorRepository(db)
        self.service_repo = ServiceRepository(db)

    def get_all_appointments(self) -> List[model.Appointment]:
        # Retrieve all appointments via repository
        return self.appointment_repo.get_all()

    def get_appointment_by_id(self, appointment_id: int) -> model.Appointment:
        # Retrieve appointment by ID or raise HTTP 404
        appointment = self.appointment_repo.get_by_id(appointment_id)
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found",
            )
        return appointment

    def create_appointment(self, appointment_schema: schemas.AppointmentCreate) -> model.Appointment:
        # Validate patient, doctor, and service existence
        patient = self.patient_repo.get_by_id(appointment_schema.patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found",
            )

        doctor = self.doctor_repo.get_by_id(appointment_schema.doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found",
            )

        service = self.service_repo.get_by_id(appointment_schema.service_id)
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical service not found",
            )

        return self.appointment_repo.create(appointment_schema)

    def delete_appointment(self, appointment_id: int) -> None:
        # Delete appointment by ID
        appointment = self.get_appointment_by_id(appointment_id)
        self.appointment_repo.delete(appointment)