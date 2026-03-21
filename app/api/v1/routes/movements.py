from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.movement import Movement, MovementCreate
from app.services.movement_service import (
    create_movement,
    get_movements,
    get_movements_by_user,
)
from app.core.security import get_current_user, get_current_admin, get_current_active_user
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Movement)
def register_movement(
    movement_in: MovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return create_movement(db, movement_in, user_id=current_user.id)


@router.get("/", response_model=list[Movement])
def list_movements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return get_movements(db)

@router.get("/me", response_model=list[Movement])
def list_my_movements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return get_movements_by_user(db, current_user.id)
