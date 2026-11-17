from datetime import datetime, time
from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator

#  USER SCHEMAS 
class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


# TOKEN SCHEMAS 
class Token(BaseModel):
    access_token: str
    token_type: str


#  DOCTOR SCHEMAS 
class DoctorBase(BaseModel):
    name: str
    specialization: str
    phone: str

class DoctorScheduleCreate(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6, description="0 = Monday, 6 = Sunday")
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.start_time >= self.end_time:
            raise ValueError("start_time must be earlier than end_time")
        return self


class DoctorScheduleResponse(BaseModel):
    id: int
    doctor_id: int
    day_of_week: int
    start_time: time
    end_time: time

    model_config = ConfigDict(from_attributes=True)

class DoctorCreate(DoctorBase):
    pass


class DoctorResponse(DoctorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


#  PATIENT SCHEMAS 
class PatientBase(BaseModel):
    name: str
    age: int
    disease: str
    doctor_id: int


class PatientCreate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: int
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)

    # --- MEDICAL SERVICE SCHEMAS ---
class MedicalServiceBase(BaseModel):
    name: str
    price: float
    duration_minutes: int


class MedicalServiceCreate(MedicalServiceBase):
    pass


class MedicalServiceResponse(MedicalServiceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- APPOINTMENT SCHEMAS ---
class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    service_id: int
    appointment_date: datetime


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentResponse(AppointmentBase):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)

 # --- APPOINTMENT STATUS SCHEMA ---
class AppointmentStatusUpdate(BaseModel):
    status: str   

# --- PATIENT HISTORY SCHEMA ---
class PatientHistoryResponse(PatientResponse):
    appointments: List[AppointmentResponse] = []

    model_config = ConfigDict(from_attributes=True)

# --- ANALYTICS SCHEMAS ---
class AnalyticsSummaryResponse(BaseModel):
    total_active_patients: int
    total_doctors: int
    total_appointments: int
    scheduled_appointments: int
    completed_appointments: int
    cancelled_appointments: int
    total_revenue: float


class DoctorAnalyticsResponse(BaseModel):
    doctor_id: int
    doctor_name: str
    specialization: str
    total_appointments: int
    completed_appointments: int
    total_revenue: float


class ServiceAnalyticsResponse(BaseModel):
    service_id: int
    service_name: str
    total_appointments: int
    total_revenue: float