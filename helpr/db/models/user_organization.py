from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped,relationship, mapped_column

from helpr.organizations.permissions import PermissionRole
from .util import Base, id_column, created_at_column, updated_at_column

class DBUserOrganization(Base):
    __tablename__ = "user_organization"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), primary_key=True)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    role: Mapped[str] = mapped_column(String)
    
    
    