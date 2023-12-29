from dataclasses import dataclass
from datetime import datetime
import string
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column
from .util import Base, id_column, created_at_column, updated_at_column

class DBChatAction(Base):
    __tablename__ = "chat_action"
    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"), primary_key=True)
    action_id: Mapped[int] = mapped_column(ForeignKey("action.id"), primary_key=True)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
  