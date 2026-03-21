from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.movement import Movement
from app.models.product import Product
from app.schemas.movement import MovementCreate


def create_movement(db: Session, movement_in: MovementCreate, user_id: int):
    product = db.query(Product).filter(Product.id == movement_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if movement_in.type == "IN":
        product.quantity += movement_in.quantity

    elif movement_in.type == "OUT":
        if product.quantity < movement_in.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough stock"
            )
        product.quantity -= movement_in.quantity

    else:
        raise HTTPException(status_code=400, detail="Invalid movement type")
   
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

def get_product_history(db: Session, product_id: int):
    return (
        db.query(Movement)
        .filter(Movement.product_id == product_id)
        .order_by(Movement.created_at.asc())
        .all()
    )

def get_product_history_with_balance(db: Session, product_id: int):
    movements = (
        db.query(Movement)
        .filter(Movement.product_id == product_id)
        .order_by(Movement.created_at.asc())
        .all()
    )

    balance = 0
    history = []

    for m in movements:
        if m.type == "IN":
            balance += m.quantity
        else:
            balance -= m.quantity

        history.append({
            "id": m.id,
            "type": m.type,
            "quantity": m.quantity,
            "product_id": m.product_id,
            "user_id": m.user_id,
            "created_at": m.created_at,
            "balance_after": balance
        })

    return history

