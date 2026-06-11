# auth.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

from auth_handler import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_active_user
)
from email_service import send_confirmation_email

router = APIRouter()


@router.post("/register", response_model=schemas.UserResponse)
async def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user or admin account. Sends a confirmation email."""

    # Check if email already exists
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered. Please use a different email."
        )

    # Create new user
    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Send confirmation email
    send_confirmation_email(
        to_email=new_user.email,
        full_name=new_user.full_name,
        role=new_user.role.value if hasattr(new_user.role, 'value') else str(new_user.role)
    )

    return new_user


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and receive a JWT access token."""

    user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(data={"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
async def get_me(
    current_user: models.User = Depends(get_current_active_user)
):
    """Get the currently logged in user profile."""
    return current_user
