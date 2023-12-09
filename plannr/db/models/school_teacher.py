from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .util import Base, created_at_column, updated_at_column

class DBSchoolTeacher(Base):
    __tablename__ = "school_teacher"
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"), primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"), primary_key=True)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    
    
    