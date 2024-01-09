from dataclasses import dataclass
from datetime import datetime
from re import S
import string
from typing import List, Optional
from click import Option
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column
from helpr.db.models.action_request import DBActionRequest
from .util import Base, id_column, created_at_column, updated_at_column

class DBMessage(Base):
    class Type:
        BOT_MESSAGE = "bot_message"
        USER_MESSAGE = "user_message"
        ACTION_REQUEST_MESSAGE = "action_request_message"
        ACTION_REQUEST_RESPONSE_MESSAGE = "action_request_response_message"
        SYSTEM_MESSAGE = "system_message"
        ACTION_RESULT_MESSAGE = "result_message"
        
    __tablename__ = "message"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    chat_session_id: Mapped[int] = mapped_column(ForeignKey("chat_session.id"))
    #TODO: the message content should be more in the future, like images and so on, so basically different type of messages, so dbmessage will be polymorph. We could also do that the content is poly so it could be {text} / {text, image} and so on..
    #maybe, we will see
    text: Mapped[str] = mapped_column(String)
    
    type: Mapped[str]
    __mapper_args__ = {
        "polymorphic_identity": "message",
        "polymorphic_on": "type",
    }
    class Config:
        orm_mode = True
    
class DBBotMessage(DBMessage):
    __tablename__ = "bot_message"
    id: Mapped[int] = mapped_column(ForeignKey("message.id"), primary_key=True)
    
    __mapper_args__ = {
        "polymorphic_identity": DBMessage.Type.BOT_MESSAGE,
    }
    

class DBActionRequestMessage(DBMessage):
    __tablename__ = "action_request_message"
    id: Mapped[int] = mapped_column(ForeignKey("message.id"), primary_key=True)
    action_request_id: Mapped[int] = mapped_column(ForeignKey("action_request.id"))
    action_request: Mapped['DBActionRequest'] = relationship(lazy="noload")
    __mapper_args__ = {
        "polymorphic_identity": DBMessage.Type.ACTION_REQUEST_MESSAGE,
    }
    
"""
class DBActionRequestResponseMessage(DBMessage):
    __tablename__ = "action_request_response_message"
    id: Mapped[int] = mapped_column(ForeignKey("message.id"), primary_key=True)
    request_message_id: Mapped[int]  = mapped_column(ForeignKey('action_request_message.id'))
    feedback: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    approved: Mapped[bool] = mapped_column(Boolean)
    next_request_id: Mapped[Optional[int]] = mapped_column(ForeignKey("action_request_message.id"), nullable=True)
    __mapper_args__ = {
        "polymorphic_identity": DBMessage.Type.ACTION_REQUEST_RESPONSE_MESSAGE,
    }
"""

#TODO: this one should be able to also have a action_run in some way right if gpt in some way should trigger an action that should run in background
class DBActionResultMessage(DBMessage):
    __tablename__ = "action_response_message"
    id: Mapped[int] = mapped_column(ForeignKey("message.id"), primary_key=True)
    output: Mapped[str] = mapped_column(String)
    action_id: Mapped[int] = mapped_column(ForeignKey('action.id'))
    action: Mapped[Optional['DBAction']] = relationship(lazy='noload') #type: ignore
    __mapper_args__ = {
        "polymorphic_identity": DBMessage.Type.ACTION_RESULT_MESSAGE,
    }
    
class DBSystemMessage(DBMessage):
    __tablename__ = "system_message"
    id: Mapped[int] = mapped_column(ForeignKey("message.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": DBMessage.Type.SYSTEM_MESSAGE,
    }

class DBUserMessage(DBMessage):
    __tablename__ = "user_message"
    id: Mapped[int] = mapped_column(ForeignKey("message.id"), primary_key=True)
  
    __mapper_args__ = {
        "polymorphic_identity": DBMessage.Type.USER_MESSAGE,
    }
    
    
    