from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import User, UserCreate
from app.services.user_service import create_user, get_user_by_email
from app.core.security import get_current_admin, get_current_active_user
from app.models.user import User as UserModel


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: UserCreate, 
    db: Session = Depends(get_db),
    urrent_user: UserModel = Depends(get_current_admin)
):
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, user_in)
    return user

@router.get("/me", response_model=User)
def get_me(
    current_user: UserModel = Depends(get_current_active_user)
):
    return current_user
