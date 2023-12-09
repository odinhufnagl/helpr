from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from .util import Base, id_column, created_at_column, updated_at_column

class DBSchool(Base):
    __tablename__ = "school"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    name = Column(String)
    code = Column(String)
    class_rooms: Mapped[List['DBClassRoom']] = relationship() #type: ignore
    class_groups: Mapped[List['DBClassGroup']] = relationship() #type: ignore
    coalition: Mapped['DBCoalition'] = relationship('DBCoalition') #type: ignore
    coalition_id: Mapped[int] = mapped_column(ForeignKey("coalition.id"))
    teachers: Mapped[List['DBTeacher']] = relationship('DBTeacher',secondary="school_teacher") #type: ignore