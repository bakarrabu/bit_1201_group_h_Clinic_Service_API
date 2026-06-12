# models.py

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from database import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"


class AppointmentStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    reviews = relationship("Review", back_populates="user")
    appointments = relationship("Appointment", back_populates="user")


class Clinic(Base):
    __tablename__ = "clinics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    website = Column(String(200))
    description = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    is_active = Column(Boolean, default=True)

    services = relationship("Service", back_populates="clinic")
    reviews = relationship("Review", back_populates="clinic")
    appointments = relationship("Appointment", back_populates="clinic")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, ForeignKey("clinics.id"))
    name = Column(String(150), nullable=False)
    description = Column(Text)
    price = Column(Float)
    is_available = Column(Boolean, default=True)

    clinic = relationship("Clinic", back_populates="services")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, ForeignKey("clinics.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer)
    comment = Column(Text)

    clinic = relationship("Clinic", back_populates="reviews")
    user = relationship("User", back_populates="reviews")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False)
    doctor_name = Column(String(150), nullable=False)
    appointment_date = Column(String(20), nullable=False)   # e.g. "2026-06-15"
    appointment_time = Column(String(10), nullable=False)   # e.g. "10:30"
    reason = Column(Text)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.pending)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="appointments")
    clinic = relationship("Clinic", back_populates="appointments")
