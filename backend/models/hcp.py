from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from core.database import Base

class HCP(Base):
    __tablename__ = "hcps"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    name       = Column(String(255), nullable=False)
    specialty  = Column(String(100))
    territory  = Column(String(100))
    email      = Column(String(255))
    phone      = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
