from datetime import datetime
from sqlalchemy import (Boolean, Column, DateTime,Float, ForeignKey, Integer, String,)
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    specialization = Column(String)
    phone = Column(String)

    patients = relationship("Patient", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    disease = Column(String)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    is_deleted = Column(Boolean, default=False)

    doctor = relationship("Doctor", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")


class MedicalService(Base):
    __tablename__ = "medical_services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    duration_minutes = Column(Integer)

    appointments = relationship("Appointment", back_populates="service")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    service_id = Column(Integer, ForeignKey("medical_services.id"))
    appointment_date = Column(DateTime)
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    service = relationship("MedicalService", back_populates="appointments")