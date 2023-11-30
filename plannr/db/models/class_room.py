from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Mapped
from .util import Base

class DBClassRoom(Base):
    __tablename__ = "class_room"
    id = Column(Integer(), primary_key=True)
    name = Column(String)
    code = Column(String)