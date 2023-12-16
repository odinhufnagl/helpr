from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from .admin_coalition import DBAdminCoalition
from .util import Base, id_column, created_at_column, updated_at_column

class DBCoalition(Base):
    __tablename__ = "coalition"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    name: Mapped[str] = mapped_column(String)
    schools: Mapped[List['DBSchool']] = relationship() #type: ignore
    admins: Mapped[List['DBAdmin']] = relationship('DBAdmin', secondary='admin_coalition') #type: ignore
    schedules: Mapped[List['DBSchedule']] = relationship() #type: ignore