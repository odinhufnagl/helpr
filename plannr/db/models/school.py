from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Mapped
from .util import Base

class DBSchool(Base):
    __tablename__ = "school"
    id = Column(Integer(), primary_key=True)
    name = Column(String)