from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
import model


class AnalyticsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_patient_count(self) -> int:
        return (
            self.db.query(func.count(model.Patient.id))
            .filter(model.Patient.is_deleted.is_(False))
            .scalar()
            or 0
        )

    def get_doctor_count(self) -> int:
        return self.db.query(func.count(model.Doctor.id)).scalar() or 0

    def get_appointment_status_counts(self) -> Dict[str, int]:
        results = (
            self.db.query(model.Appointment.status, func.count(model.Appointment.id))
            .group_by(model.Appointment.status)
            .all()
        )
        status_map = {"scheduled": 0, "completed": 0, "cancelled": 0}
        for status_name, count in results:
            status_map[status_name] = count
        return status_map

    def get_total_revenue(self) -> float:
        total = (
            self.db.query(func.sum(model.MedicalService.price))
            .select_from(model.Appointment)
            .join(model.MedicalService)
            .filter(model.Appointment.status == "completed")
            .scalar()
        )
        return float(total or 0.0)

    def get_doctor_analytics(self) -> List[Dict[str, Any]]:
        doctors = self.db.query(model.Doctor).all()
        analytics = []

        for doc in doctors:
            total_appts = (
                self.db.query(func.count(model.Appointment.id))
                .filter(model.Appointment.doctor_id == doc.id)
                .scalar()
                or 0
            )
            completed_appts = (
                self.db.query(func.count(model.Appointment.id))
                .filter(
                    model.Appointment.doctor_id == doc.id,
                    model.Appointment.status == "completed",
                )
                .scalar()
                or 0
            )
            revenue = (
                self.db.query(func.sum(model.MedicalService.price))
                .select_from(model.Appointment)
                .join(model.MedicalService)
                .filter(
                    model.Appointment.doctor_id == doc.id,
                    model.Appointment.status == "completed",
                )
                .scalar()
                or 0.0
            )

            analytics.append(
                {
                    "doctor_id": doc.id,
                    "doctor_name": doc.name,
                    "specialization": doc.specialization,
                    "total_appointments": total_appts,
                    "completed_appointments": completed_appts,
                    "total_revenue": float(revenue),
                }
            )

        return analytics

    def get_service_analytics(self) -> List[Dict[str, Any]]:
        services = self.db.query(model.MedicalService).all()
        analytics = []

        for srv in services:
            total_appts = (
                self.db.query(func.count(model.Appointment.id))
                .filter(model.Appointment.service_id == srv.id)
                .scalar()
                or 0
            )
            completed_appts = (
                self.db.query(func.count(model.Appointment.id))
                .filter(
                    model.Appointment.service_id == srv.id,
                    model.Appointment.status == "completed",
                )
                .scalar()
                or 0
            )
            revenue = completed_appts * srv.price

            analytics.append(
                {
                    "service_id": srv.id,
                    "service_name": srv.name,
                    "total_appointments": total_appts,
                    "total_revenue": float(revenue),
                }
            )

        return analytics