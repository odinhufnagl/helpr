from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from .util import Base, id_column, created_at_column, updated_at_column

class DBAdminCoalition(Base):
    __tablename__ = "admin_coalition"
    admin_id: Mapped[int] = mapped_column(ForeignKey("admin.id"), primary_key=True)
    coalition_id: Mapped[int] = mapped_column(ForeignKey("coalition.id"), primary_key=True)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    
    
    