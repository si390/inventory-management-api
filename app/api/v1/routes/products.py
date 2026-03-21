from typing import List
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.product_service import get_products, get_product, create_product
from app.services.movement_service import get_product_history
from app.schemas.movement import Movement
from app.core.security import get_current_user, get_current_active_user
from app.models.user import User
from app.schemas.product import ProductCreate, Product

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[Product])
def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_products(db)


@router.get("/{product_id}", response_model=Product)
def retrieve_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/{product_id}/history", response_model=list[Movement])
def product_history(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    history = get_product_history(db, product_id)
    return history

@router.post("/", response_model=Product, status_code=201)
def create_new_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product_in)
