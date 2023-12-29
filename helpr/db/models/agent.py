from dataclasses import dataclass
from datetime import datetime
import string
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column
from .util import Base, id_column, created_at_column, updated_at_column

class DBAgent(Base):
    __tablename__ = "agent"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    organization: Mapped['DBOrganization'] = relationship() #type: ignore
    #TODO: this should be its own table so it can be polymorphism like IndexLocationServer, or IndexLocationPath
    index_id: Mapped[int] = mapped_column(ForeignKey('index.id'))
    index: Mapped['DBIndex'] = relationship() #type: ignore
    