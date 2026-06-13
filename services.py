# services.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

import models
from database import get_db
from auth_handler import get_current_user

router = APIRouter()


# ── Schemas ───────────────────────────────────────────────────────────────────

class ServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: bool = True


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None


class ServiceResponse(BaseModel):
    id: int
    clinic_id: int
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: bool

    class Config:
        from_attributes = True


# ── GET all services ──────────────────────────────────────────────────────────

@router.get("/", response_model=List[ServiceResponse])
async def get_all_services(
    clinic_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all services. Optionally filter by clinic_id."""
    query = db.query(models.Service)
    if clinic_id:
        query = query.filter(models.Service.clinic_id == clinic_id)
    return query.all()


# ── GET single service ────────────────────────────────────────────────────────

@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(service_id: int, db: Session = Depends(get_db)):
    """Get one service by ID."""
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


# ── CREATE service ────────────────────────────────────────────────────────────

@router.post("/{clinic_id}/services", response_model=ServiceResponse, status_code=201)
async def create_service(
    clinic_id: int,
    service: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Add a new service to a clinic. Admin only."""
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    clinic = db.query(models.Clinic).filter(models.Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")

    new_service = models.Service(
        clinic_id=clinic_id,
        name=service.name,
        description=service.description,
        price=service.price,
        is_available=service.is_available
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service


# ── UPDATE service ────────────────────────────────────────────────────────────

@router.put("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: int,
    updates: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update a service. Admin only."""
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    if updates.name is not None:
        service.name = updates.name
    if updates.description is not None:
        service.description = updates.description
    if updates.price is not None:
        service.price = updates.price
    if updates.is_available is not None:
        service.is_available = updates.is_available

    db.commit()
    db.refresh(service)
    return service


# ── DELETE service ────────────────────────────────────────────────────────────

@router.delete("/{service_id}", status_code=204)
async def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete a service. Admin only."""
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    db.delete(service)
    db.commit()
    return None
