from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, relationship
from .util import Base, id_column, created_at_column, updated_at_column

class DBOrganization(Base):
    __tablename__ = "organization"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    users: Mapped[Optional[List['DBUser']]] = relationship('DBUser', secondary='user_organization') #type: ignore
    
    
    
    