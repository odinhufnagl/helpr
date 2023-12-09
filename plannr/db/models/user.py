from datetime import datetime
from typing import Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from .util import Base, id_column, created_at_column, updated_at_column

class DBUser(Base):
    __tablename__ = "user"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    email: Mapped[str] = mapped_column(String) #TODO: add email validation #TODO: email should be primary-key right?, or at least not two users with same email
    password: Mapped[str] = mapped_column(String) #TODO: should not be visible when fething
    