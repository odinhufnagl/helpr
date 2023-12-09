import datetime
from typing import Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped
from sqlalchemy.orm import relationship
from .util import Base, id_column, created_at_column, updated_at_column
from sqlalchemy.orm import mapped_column
from datetime import datetime

class DBClassRoom(Base):
    __tablename__ = "class_room"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    name: Mapped[str] = mapped_column(String)
    code: Mapped[str] = mapped_column(String)
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"))
    school: Mapped['DBSchool'] = relationship() # type: ignore