
from dataclasses import dataclass
from datetime import datetime
import string
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column
from helpr.db.models.action_run import DBActionRun
from .util import Base, id_column, created_at_column, updated_at_column

class DBActionRequest(Base):
    __tablename__ = "action_request"
    id: Mapped[int] = id_column()
    action_id: Mapped[int] = mapped_column(ForeignKey('action.id'))
    action: Mapped[Optional['DBAction']] = relationship(lazy='noload') #type: ignore
    input: Mapped[str] = mapped_column(String) #TODO: this should be a json-object or something
    response_id: Mapped[Optional[int]] = mapped_column(ForeignKey('action_request_response.id'), nullable=True)
    response: Mapped[Optional['DBActionRequestResponse']] = relationship(lazy='noload', foreign_keys=[response_id])
    action_run_id: Mapped[Optional[int]] = mapped_column(ForeignKey("action_run.id"), nullable=True)
    
class DBActionRequestResponse(Base):
    __tablename__ = "action_request_response"
    id: Mapped[int] = id_column()
    action_request_id: Mapped[int]  = mapped_column(ForeignKey('action_request.id'))
    feedback: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    approved: Mapped[bool] = mapped_column(Boolean)
    next_action_request_id: Mapped[Optional[int]] = mapped_column(ForeignKey('action_request.id'), nullable=True)
    action_run_id: Mapped[Optional[int]] = mapped_column(ForeignKey("action_run.id"), nullable=True)
    action_run: Mapped[Optional['DBActionRun']] = relationship(lazy="noload")
    