from datetime import datetime
from enum import Enum
import json
from typing import Any, Optional
from sqlalchemy import BLOB, JSON, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from .util import Base, id_column, created_at_column, updated_at_column

class DBFeedback(Base):        
    __tablename__ = "feedback"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    priority: Mapped[int] = mapped_column(Integer)
    schedule_id: Mapped[int] = mapped_column(ForeignKey('schedule.id'))
    schedule: Mapped['DBSchedule'] = relationship() #type: ignore
    used: Mapped[bool] = mapped_column(Boolean, default=False)