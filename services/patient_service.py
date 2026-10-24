from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.doctor_repository import DoctorRepository
from repositories.patient_repository import PatientRepository
import model
import schemas


class PatientService:
    def __init__(self, db: Session):
        self.patient_repo = PatientRepository(db)
        self.doctor_repo = DoctorRepository(db)

    def get_all_patients(self) -> List[model.Patient]:
        # Retrieve active patients via repository
        return self.patient_repo.get_all_active()

    def get_patient_by_id(self, patient_id: int) -> model.Patient:
        # Retrieve active patient by ID or raise HTTP 404
        patient = self.patient_repo.get_by_id(patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found",
            )
        return patient

    def create_patient(self, patient_schema: schemas.PatientCreate) -> model.Patient:
        # Validate doctor existence before creating patient
        doctor = self.doctor_repo.get_by_id(patient_schema.doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found",
            )
        return self.patient_repo.create(patient_schema)

    def update_patient(
        self, patient_id: int, patient_update: schemas.PatientCreate
    ) -> model.Patient:
        # Validate patient and doctor existence before updating
        patient = self.get_patient_by_id(patient_id)
        doctor = self.doctor_repo.get_by_id(patient_update.doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found",
            )
        return self.patient_repo.update(patient, patient_update)

    def soft_delete_patient(self, patient_id: int) -> None:
        # Perform soft deletion on patient
        patient = self.get_patient_by_id(patient_id)
        self.patient_repo.soft_delete(patient)