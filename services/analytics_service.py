from typing import List, Dict, Any
from sqlalchemy.orm import Session
from repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:
    def __init__(self, db: Session):
        self.analytics_repo = AnalyticsRepository(db)

    def get_summary(self) -> Dict[str, Any]:
        patient_count = self.analytics_repo.get_patient_count()
        doctor_count = self.analytics_repo.get_doctor_count()
        status_counts = self.analytics_repo.get_appointment_status_counts()
        total_revenue = self.analytics_repo.get_total_revenue()

        total_appointments = sum(status_counts.values())

        return {
            "total_active_patients": patient_count,
            "total_doctors": doctor_count,
            "total_appointments": total_appointments,
            "scheduled_appointments": status_counts.get("scheduled", 0),
            "completed_appointments": status_counts.get("completed", 0),
            "cancelled_appointments": status_counts.get("cancelled", 0),
            "total_revenue": total_revenue,
        }

    def get_doctors_analytics(self) -> List[Dict[str, Any]]:
        return self.analytics_repo.get_doctor_analytics()

    def get_services_analytics(self) -> List[Dict[str, Any]]:
        return self.analytics_repo.get_service_analytics()