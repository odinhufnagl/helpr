from dataclasses import dataclass
from datetime import datetime
from re import M
import string
from typing import Dict, List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column
from .util import Base, id_column, created_at_column, updated_at_column

class DBActionRun(Base):
    class Status:
        CREATED = "created"
        RUNNING = "running"
        FINISHED = "finished"
        ERROR = "error"
        
    __tablename__ = "action_run"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    action_id: Mapped[int] = mapped_column(ForeignKey('action.id'))
    action: Mapped['DBAction'] = relationship(lazy="noload") #type: ignore
    input: Mapped[str] = Column(String, nullable=True) # type: ignore
    output: Mapped[str] = Column(String, nullable=True) # type: ignore
    status: Mapped[Status] = Column(String, default=Status.CREATED)
    
