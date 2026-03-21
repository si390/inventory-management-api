from pydantic import BaseModel
from enum import Enum

class MovementType(str, Enum):
    IN = "IN"
    OUT = "OUT"

class MovementBase(BaseModel):
    type: MovementType
    quantity: int
    product_id: int


class MovementCreate(MovementBase):
    pass


class Movement(MovementBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True