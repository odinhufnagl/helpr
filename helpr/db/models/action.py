from dataclasses import dataclass
from datetime import datetime
import string
from typing import Dict, List, Optional
from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer, String, null
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column

from helpr.db.models.field import  DBField
from .util import Base, id_column, created_at_column, updated_at_column



#TODO: is poly here overkill, sure it makes it so that not everything can break by someone for example updating the key in {'url': "www.com"} (which would be an ActionField), and breaking the entire function. But at the same time those could be "hardcoded"

class DBAction(Base):
    class Type:
        ADD = 'add'
        MULTIPLY = 'multiply'
        POST_REQUEST = 'post_request'
        
    __tablename__ = "action"
    id: Mapped[int] = id_column()
    type: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    feedback_required: Mapped[bool] = mapped_column(Boolean)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    organization_id: Mapped[Optional[int]] = mapped_column(ForeignKey('organization.id'), nullable=True)
  
    chats: Mapped[Optional[List['DBAction']]] = relationship('DBChat', secondary='chat_action') #type: ignore
  
    type: Mapped[str]
    __mapper_args__ = {
        "polymorphic_identity": "action",
        "polymorphic_on": "type",
    }
    
class DBAddAction(DBAction):
    __tablename__ = "add_action"
    id: Mapped[int] = mapped_column(ForeignKey("action.id"), primary_key=True)
    
    __mapper_args__ = {
        "polymorphic_identity": DBAction.Type.ADD,
    }
    
class DBPostRequestAction(DBAction):
    __tablename__ = "post_request_action"
    id: Mapped[int] = mapped_column(ForeignKey("action.id"), primary_key=True)
    url_field_id: Mapped[int] = mapped_column(ForeignKey('field.id'))
    url_field: Mapped[DBField] = relationship('DBField', foreign_keys=[url_field_id], lazy='noload')
    headers_field_id: Mapped[int] = mapped_column(ForeignKey('field.id'))
    headers_field: Mapped[DBField] = relationship('DBField', foreign_keys=[headers_field_id], lazy='noload')
    body_input_struct: Mapped[Dict | None] = mapped_column(JSON, nullable=True)
    result_output_struct: Mapped[Dict | None] = mapped_column(JSON, nullable=True)    
    __mapper_args__ = {
        "polymorphic_identity": DBAction.Type.POST_REQUEST,
    }
    
