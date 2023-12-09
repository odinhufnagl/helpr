from datetime import datetime
from typing import Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from .util import Base, id_column, created_at_column, updated_at_column

class DBCourse(Base):
    __tablename__ = "course"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    name: Mapped[str] = mapped_column(String)
    code: Mapped[str] = mapped_column(String)
    coalition_id: Mapped[int] = mapped_column(ForeignKey("coalition.id"))
    coalition: Mapped['DBCoalition'] = relationship() #type: ignore