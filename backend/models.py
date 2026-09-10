from sqlalchemy import Column, Integer, String
from database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="Applied")