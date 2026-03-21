from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_movements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {"message": "Movements protected"}