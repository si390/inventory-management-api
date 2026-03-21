from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken
import secrets


REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_refresh_token(db: Session, user_id: int):
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    db_token = RefreshToken(
        token=token,
        user_id=user_id,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def verify_refresh_token(db: Session, token: str):
    db_token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == token, RefreshToken.revoked == False)
        .first()
    )

    if not db_token:
        return None

    if db_token.expires_at < datetime.utcnow():
        return None

    return db_token


def revoke_refresh_token(db: Session, token: str):
    db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if db_token:
        db_token.revoked = True
        db.commit()