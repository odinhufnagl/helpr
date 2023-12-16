from datetime import datetime
from enum import Enum
from typing import List, Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from db.models.coalition import DBCoalition
from .util import Base, id_column, created_at_column, updated_at_column


class DBSchedule(Base):
    class State(Enum):
        ONGOING = "ongoing"
        CREATING = "creating"
        FINISHED = "finished"
        
    __tablename__ = "schedule"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    state: Mapped[State] = mapped_column(String, default=State.CREATING.name)
    coalition_id: Mapped[int] = mapped_column(ForeignKey('coalition.id'))
    coalition: Mapped['DBCoalition'] = relationship()  # type: ignore
    events: Mapped[List['DBEvent']] = relationship()  # type: ignore
