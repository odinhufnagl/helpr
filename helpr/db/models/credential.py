from dataclasses import dataclass
from datetime import datetime
import string
from typing import Dict, List, Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column
from .util import Base, id_column, created_at_column, updated_at_column

class DBCredential(Base):
    __tablename__ = "credential"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    data: Mapped[Dict | None] = Column(JSON, nullable=True) # type: ignore
    provider: Mapped[str] = mapped_column(String)
    organization_id: Mapped[int] = mapped_column(ForeignKey('organization.id'))