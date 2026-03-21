from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    quantity: int = 0
    price: float = 0.0


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True