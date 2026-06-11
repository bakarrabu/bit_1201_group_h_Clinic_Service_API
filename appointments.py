# appointments.py
# Book a doctor appointment at a specific clinic

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

import models
from database import get_db
from auth_handler import get_current_user

router = APIRouter()


# ── Schemas ───────────────────────────────────────────────────────────────────

class AppointmentCreate(BaseModel):
    clinic_id: int
    doctor_name: str
    appointment_date: str   # format: YYYY-MM-DD  e.g. 2026-06-15
    appointment_time: str   # format: HH:MM       e.g. 10:30
    reason: Optional[str] = None


class AppointmentUpdate(BaseModel):
    doctor_name: Optional[str] = None
    appointment_date: Optional[str] = None
    appointment_time: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: int
    user_id: int
    clinic_id: int
    doctor_name: str
    appointment_date: str
    appointment_time: str
    reason: Optional[str] = None
    status: str
    notes: Optional[str] = None

    class Config:
        from_attributes = True


# ── BOOK appointment ──────────────────────────────────────────────────────────

@router.post("/", response_model=AppointmentResponse, status_code=201)
async def book_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Book a doctor appointment at a clinic. Login required."""

    # Check clinic exists
    clinic = db.query(models.Clinic).filter(
        models.Clinic.id == data.clinic_id,
        models.Clinic.is_active == True
    ).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")

    appointment = models.Appointment(
        user_id=current_user.id,
        clinic_id=data.clinic_id,
        doctor_name=data.doctor_name,
        appointment_date=data.appointment_date,
        appointment_time=data.appointment_time,
        reason=data.reason,
        status=models.AppointmentStatus.pending
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


# ── GET all appointments ──────────────────────────────────────────────────────

@router.get("/", response_model=List[AppointmentResponse])
async def get_appointments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get appointments. Admins see all. Users see only their own."""
    if current_user.role == models.UserRole.admin:
        return db.query(models.Appointment).all()
    return db.query(models.Appointment).filter(
        models.Appointment.user_id == current_user.id
    ).all()


# ── GET single appointment ────────────────────────────────────────────────────

@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get one appointment by ID."""
    appt = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appt.user_id != current_user.id and current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Not your appointment")
    return appt


# ── UPDATE appointment ────────────────────────────────────────────────────────

@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: int,
    updates: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update or cancel an appointment."""
    appt = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appt.user_id != current_user.id and current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Not your appointment")

    if updates.doctor_name: appt.doctor_name = updates.doctor_name
    if updates.appointment_date: appt.appointment_date = updates.appointment_date
    if updates.appointment_time: appt.appointment_time = updates.appointment_time
    if updates.reason: appt.reason = updates.reason
    if updates.notes: appt.notes = updates.notes
    if updates.status:
        try:
            appt.status = models.AppointmentStatus(updates.status)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid status. Use: pending, confirmed, cancelled, completed")

    db.commit()
    db.refresh(appt)
    return appt


# ── CANCEL appointment ────────────────────────────────────────────────────────

@router.put("/{appointment_id}/cancel", response_model=AppointmentResponse)
async def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Cancel an appointment quickly."""
    appt = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appt.user_id != current_user.id and current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Not your appointment")

    appt.status = models.AppointmentStatus.cancelled
    db.commit()
    db.refresh(appt)
    return appt


# ── DELETE appointment ────────────────────────────────────────────────────────

@router.delete("/{appointment_id}", status_code=204)
async def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete an appointment. Admin only."""
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    appt = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appt)
    db.commit()
    return None
