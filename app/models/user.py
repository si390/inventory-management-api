from sqlalchemy import Column, Integer, String, Boolean, Enum
import enum
from app.db.session import Base

class UserRole(str, enum.Enum):
    admin = "admin"
    supervisor = "supervisor"
    operator = "operator"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.operator)
