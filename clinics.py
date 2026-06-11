# clinics.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from auth_handler import get_current_user
import models
import schemas

router = APIRouter()


# ── GET all clinics — anyone can see ─────────────────────────────────────────
@router.get("/", response_model=List[schemas.ClinicResponse])
async def get_clinics(db: Session = Depends(get_db)):
    """List all clinics. No login required."""
    return db.query(models.Clinic).filter(models.Clinic.is_active == True).all()


# ── GET one clinic — anyone can see ──────────────────────────────────────────
@router.get("/{clinic_id}", response_model=schemas.ClinicResponse)
async def get_clinic(clinic_id: int, db: Session = Depends(get_db)):
    """Get one clinic by ID. No login required."""
    clinic = db.query(models.Clinic).filter(models.Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    return clinic


# ── CREATE clinic — ADMIN ONLY ────────────────────────────────────────────────
@router.post("/", response_model=schemas.ClinicResponse, status_code=201)
async def create_clinic(
    clinic: schemas.ClinicCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new clinic. ADMIN ONLY."""
    if current_user.role != models.UserRole.admin:
        raise HTTPException(
            status_code=403,
            detail="Access denied. Only admins can create clinics."
        )
    new_clinic = models.Clinic(**clinic.dict())
    db.add(new_clinic)
    db.commit()
    db.refresh(new_clinic)
    return new_clinic


# ── UPDATE clinic — ADMIN ONLY ────────────────────────────────────────────────
@router.put("/{clinic_id}", response_model=schemas.ClinicResponse)
async def update_clinic(
    clinic_id: int,
    updates: schemas.ClinicCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update a clinic. ADMIN ONLY."""
    if current_user.role != models.UserRole.admin:
        raise HTTPException(
            status_code=403,
            detail="Access denied. Only admins can update clinics."
        )
    clinic = db.query(models.Clinic).filter(models.Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")

    for key, value in updates.dict(exclude_unset=True).items():
        setattr(clinic, key, value)

    db.commit()
    db.refresh(clinic)
    return clinic


# ── DELETE clinic — ADMIN ONLY ────────────────────────────────────────────────
@router.delete("/{clinic_id}", status_code=204)
async def delete_clinic(
    clinic_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete a clinic. ADMIN ONLY."""
    if current_user.role != models.UserRole.admin:
        raise HTTPException(
            status_code=403,
            detail="Access denied. Only admins can delete clinics."
        )
    clinic = db.query(models.Clinic).filter(models.Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")

    db.delete(clinic)
    db.commit()
    return None
