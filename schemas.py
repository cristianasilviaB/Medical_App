from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)