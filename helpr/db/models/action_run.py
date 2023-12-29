from dataclasses import dataclass
from datetime import datetime
import string
from typing import Dict, List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column
from .util import Base, id_column, created_at_column, updated_at_column

class DBActionRun(Base):
    __tablename__ = "action_run"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    action_id: Mapped[int] = mapped_column(ForeignKey('action.id'))
    action: Mapped['DBAction'] = relationship() #type: ignore
    input: Mapped[Dict | None] = Column(JSON, nullable=True) # type: ignore
    output: Mapped[Dict | None] = Column(JSON, nullable=True) # type: ignore