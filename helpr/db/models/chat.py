from dataclasses import dataclass
from datetime import datetime
import string
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String, ARRAY
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column
from .util import Base, id_column, created_at_column, updated_at_column

class DBChat(Base):
    __tablename__ = "chat"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    organization: Mapped['DBOrganization'] = relationship() #type: ignore
    agent_id: Mapped[int] = mapped_column(ForeignKey("agent.id"))
    agent: Mapped['DBAgent'] = relationship() #type: ignore
    name: Mapped[str] = mapped_column(String)
    system_prompt: Mapped[str] = mapped_column(String)
    available_actions: Mapped[Optional[List['DBAction']]] = relationship('DBAction', secondary='chat_action') #type: ignore
    
    
    