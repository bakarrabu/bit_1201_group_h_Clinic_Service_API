# schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    user = "user"


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.user


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class ClinicCreate(BaseModel):
    name: str
    address: str
    city: str
    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]
    description: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]


class ClinicResponse(BaseModel):
    id: int
    name: str
    address: str
    city: str

    class Config:
        orm_mode = True


class ReviewCreate(BaseModel):
    clinic_id: int
    rating: int
    comment: Optional[str] = None


class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    clinic_id: int
    user_id: int
    rating: int
    comment: Optional[str] = None

    class Config:
        orm_mode = True


# ── Stats & Analytics Schemas ─────────────────────────────────────────────────

class SummaryStats(BaseModel):
    total_clinics: int
    active_clinics: int
    inactive_clinics: int
    total_users: int
    total_reviews: int
    total_services: int
    overall_average_rating: float


class ClinicRankingResponse(BaseModel):
    rank: int
    clinic_id: int
    clinic_name: str
    city: str
    average_rating: float
    review_count: int


class RatingDistribution(BaseModel):
    stars: int
    count: int
    percentage: float


class CityStats(BaseModel):
    city: str
    clinic_count: int
    average_rating: Optional[float] = None