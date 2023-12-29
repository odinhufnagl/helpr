from dataclasses import dataclass
from datetime import datetime
import string
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column
from .util import Base, id_column, created_at_column, updated_at_column

class DBIndex(Base):
    __tablename__ = "index"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    organization: Mapped['DBOrganization'] = relationship() #type: ignore
    #TODO: this should be its own table so it can be polymorphism like IndexLocationServer, or IndexLocationPath
    location: Mapped[str] = mapped_column(String)
    