from dataclasses import dataclass
from datetime import datetime
import string
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column
from .util import Base, id_column, created_at_column, updated_at_column

class DBChatSession(Base):
    __tablename__ = "chat_session"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"))
    chat: Mapped['DBChat'] = relationship() #type: ignore
    #session: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    messages: Mapped[Optional[List['DBMessage']]] = relationship('DBMessage') #type: ignore
    