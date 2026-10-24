from datetime import timedelta
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

        # Calculate requested start and end time window
        requested_start = appointment_schema.appointment_date.replace(tzinfo=None)
        requested_end = requested_start + timedelta(minutes=service.duration_minutes)

        # Retrieve existing appointments for the requested doctor
        existing_appointments = self.appointment_repo.get_by_doctor_id(appointment_schema.doctor_id)

        # Check for time overlap
        for existing in existing_appointments:
            if existing.status == "cancelled":
                continue

            existing_service = self.service_repo.get_by_id(existing.service_id)
            if not existing_service:
                continue

            existing_start = existing.appointment_date.replace(tzinfo=None)
            existing_end = existing_start + timedelta(minutes=existing_service.duration_minutes)

            # Overlap condition: requested_start < existing_end AND requested_end > existing_start
            if requested_start < existing_end and requested_end > existing_start:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Doctor is not available at the requested time slot due to an overlapping appointment",
                )

        return self.appointment_repo.create(appointment_schema)

    def delete_appointment(self, appointment_id: int) -> None:
        # Delete appointment by ID
        appointment = self.get_appointment_by_id(appointment_id)
        self.appointment_repo.delete(appointment)