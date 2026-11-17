from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import model
import schemas
from repositories.schedule_repository import ScheduleRepository
from repositories.doctor_repository import DoctorRepository


class ScheduleService:
    def __init__(self, db: Session):
        self.schedule_repo = ScheduleRepository(db)
        self.doctor_repo = DoctorRepository(db)

    def add_schedule(self, doctor_id: int, schedule_data: schemas.DoctorScheduleCreate) -> model.DoctorSchedule:
        doctor = self.doctor_repo.get_by_id(doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found",
            )

        existing_shifts = self.schedule_repo.get_by_doctor_and_day(
            doctor_id, schedule_data.day_of_week
        )
        for shift in existing_shifts:
            if schedule_data.start_time < shift.end_time and schedule_data.end_time > shift.start_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Schedule overlaps with an existing working shift on this day",
                )

        new_schedule = model.DoctorSchedule(
            doctor_id=doctor_id,
            day_of_week=schedule_data.day_of_week,
            start_time=schedule_data.start_time,
            end_time=schedule_data.end_time,
        )
        return self.schedule_repo.create(new_schedule)

    def get_doctor_schedules(self, doctor_id: int) -> List[model.DoctorSchedule]:
        doctor = self.doctor_repo.get_by_id(doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found",
            )
        return self.schedule_repo.get_by_doctor(doctor_id)

    def delete_schedule(self, schedule_id: int) -> None:
        schedule = self.schedule_repo.get_by_id(schedule_id)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Schedule entry not found",
            )
        self.schedule_repo.delete(schedule)