from sqlalchemy.orm import Session
from app.models.movement import Movement
from app.schemas.movement import MovementCreate


def create_movement(db: Session, movement_in: MovementCreate, user_id: int):
    movement = Movement(
        **movement_in.dict(),
        user_id=user_id
    )
    db.add(movement)
    db.commit()
    db.refresh(movement)
    return movement


def get_movements(db: Session):
    return db.query(Movement).all()


def get_movements_by_user(db: Session, user_id: int):
    return db.query(Movement).filter(Movement.user_id == user_id).all()