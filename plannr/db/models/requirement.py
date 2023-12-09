from datetime import datetime
from enum import Enum
import json
from typing import Any, Optional
from sqlalchemy import BLOB, JSON, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from .util import Base, id_column, created_at_column, updated_at_column

class DBRequirement(Base):
    class Type(Enum):
        #TODO: these are just dummy requirements
        TEACHER_EVENT = "teacher_event"
        CLASS_GROUP_EVENT = "class_group_event" 
        
    __tablename__ = "requirement"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    priority: Mapped[int] = mapped_column(Integer)
    params: Mapped[Any] = mapped_column(JSON)
    type: Mapped[Type] = mapped_column(String)
    coalition_id: Mapped[int] = mapped_column(ForeignKey("coalition.id"))
    coalition: Mapped['DBCoalition'] = relationship() #type: ignore
