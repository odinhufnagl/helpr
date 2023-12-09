from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from .admin_coalition import DBAdminCoalition
from .util import Base, id_column, created_at_column, updated_at_column

class DBAdmin(Base):
    __tablename__ = "admin"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped['DBUser'] = relationship() #type: ignore
    coalitions: Mapped[List['DBCoalition']] = relationship('DBCoalition', secondary='admin_coalition') #type: ignore
    
    
    