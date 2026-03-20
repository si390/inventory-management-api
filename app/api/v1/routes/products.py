from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.product_service import get_products, create_product
from app.schemas.product import ProductCreate, Product

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[Product])
def list_products(db: Session = Depends(get_db)):
    return get_products(db)

@router.post("/", response_model=Product)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)