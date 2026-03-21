from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)  # "IN" o "OUT"
    quantity = Column(Integer, nullable=False)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product = relationship("Product")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")
