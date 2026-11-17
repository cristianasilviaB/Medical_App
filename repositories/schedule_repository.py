from typing import List, Optional
from sqlalchemy.orm import Session
import model


class ScheduleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, schedule: model.DoctorSchedule) -> model.DoctorSchedule:
        self.db.add(schedule)
        self.db.commit()
        self.db.refresh(schedule)
        return schedule

    def get_by_doctor(self, doctor_id: int) -> List[model.DoctorSchedule]:
        return (
            self.db.query(model.DoctorSchedule)
            .filter(model.DoctorSchedule.doctor_id == doctor_id)
            .order_by(model.DoctorSchedule.day_of_week, model.DoctorSchedule.start_time)
            .all()
        )

    def get_by_doctor_and_day(self, doctor_id: int, day_of_week: int) -> List[model.DoctorSchedule]:
        return (
            self.db.query(model.DoctorSchedule)
            .filter(
                model.DoctorSchedule.doctor_id == doctor_id,
                model.DoctorSchedule.day_of_week == day_of_week,
            )
            .all()
        )

    def get_by_id(self, schedule_id: int) -> Optional[model.DoctorSchedule]:
        return (
            self.db.query(model.DoctorSchedule)
            .filter(model.DoctorSchedule.id == schedule_id)
            .first()
        )

    def delete(self, schedule: model.DoctorSchedule) -> None:
        self.db.delete(schedule)
        self.db.commit()