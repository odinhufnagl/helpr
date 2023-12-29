from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped,relationship, mapped_column
from helpr.db.models.variable import DBVariable

from helpr.organizations.permissions import PermissionRole
from .util import Base, id_column, created_at_column, updated_at_column

class DBField(Base):
    __tablename__ = "field"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    variable_id: Mapped[Optional[int]] = mapped_column(ForeignKey("variable.id"), nullable=True)
    variable: Mapped[Optional[DBVariable]] = relationship('DBVariable', foreign_keys=[variable_id], lazy='selectin')
    value: Mapped[Optional[Dict | None]] = mapped_column(JSON, nullable=True)
    
    def get_value(self):
        if self.variable:
            return self.variable.value
        return self.value
        
    
    
    