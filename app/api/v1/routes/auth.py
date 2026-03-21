from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.user import UserLogin
from app.schemas.auth import Token
from app.services.user_service import authenticate_user
from app.core.security import create_access_token
from app.core.config import settings
from app.services.refresh_token_service import create_refresh_token,  verify_refresh_token



router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_in.email, user_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(db, user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token.token,
        "token_type": "bearer"

    }

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    db_token = verify_refresh_token(db, refresh_token)
    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token(subject=str(db_token.user_id))

    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
