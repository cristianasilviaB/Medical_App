from pydantic import BaseModel, ConfigDict
from datetime import datetime

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