from pydantic import BaseModel


class MovementBase(BaseModel):
    type: str  # "IN" o "OUT"
    quantity: int
    product_id: int


class MovementCreate(MovementBase):
    pass


class Movement(MovementBase):
    id: int

    class Config:
        orm_mode = True