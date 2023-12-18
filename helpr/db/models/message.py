from dataclasses import dataclass
from datetime import datetime
import string
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column
from .util import Base, id_column, created_at_column, updated_at_column


#TODO: should be polymorphism if this is a message from the bot or from the client
class DBMessage(Base):
    __tablename__ = "message"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    chat_session_id: Mapped[int] = mapped_column(ForeignKey("chat_session.id"))
    #TODO: the message content should be more in the future, like images and so on, so basically different type of messages, so dbmessage will be polymorph. We could also do that the content is poly so it could be {text} / {text, image} and so on..
    #maybe, we will see
    text: Mapped[String] = mapped_column(String)
    
    