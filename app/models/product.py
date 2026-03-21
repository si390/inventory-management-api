from sqlalchemy import Column, Integer, String, Float
from app.db.session import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0.0)