from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from click import Option
from pydantic import BaseModel
from helpr.db.models.message import DBActionRequestMessage, DBBotMessage, DBMessage, DBSystemMessage, DBActionResultMessage
from helpr.schemas.action import ActionSchema
from sqlalchemy.orm import make_transient, make_transient_to_detached
from helpr.schemas.action_request import ActionRequestSchema
from helpr.schemas.base import BaseSchema



class MessageSchema(BaseSchema):
    class Type:
        BOT_MESSAGE = "bot_message"
        USER_MESSAGE = "user_message"
        ACTION_REQUEST_MESSAGE = "action_request_message"
        ACTION_REQUEST_RESPONSE_MESSAGE = "action_request_response_message"
        SYSTEM_MESSAGE = "system_message"
        ACTION_RESULT_MESSAGE = "result_message"
    id: int
    chat_session_id: int
    created_at: datetime
    updated_at: datetime
    text: Optional[str]
    type: str = ""


    def from_model(model: DBMessage):
    
        if model.type == DBMessage.Type.BOT_MESSAGE:
            return BotMessageSchema.from_model(model)
        if model.type == DBMessage.Type.USER_MESSAGE:
            return UserMessageSchema.from_model(model)
        if model.type == DBMessage.Type.ACTION_REQUEST_MESSAGE:
            return ActionRequestMessageSchema.from_model(model)
        if model.type == DBMessage.Type.ACTION_RESULT_MESSAGE:
            return ActionResultMessageSchema.from_model(model)
        """ if model.type == DBMessage.Type.ACTION_REQUEST_RESPONSE_MESSAGE:
            return ActionRequestResponseMessageSchema.from_model(model)"""


class dto:
    class CreateMessage(BaseModel):
        text: Optional[str] = None
        chat_session_id: int

    class CreateBotMessage(CreateMessage):
        pass

    class CreateUserMessage(CreateMessage):
        pass
    
    class CreateActionRequestMessage(CreateMessage):
        action_request_id: int
        
    class CreateActionResultMessage(CreateMessage):
        output: str
        action_id: int
        
class BotMessageSchema(MessageSchema):
    text: str
    type: str = MessageSchema.Type.BOT_MESSAGE
    def from_model(model: DBBotMessage):
        return BotMessageSchema(id=model.id, text=model.text, chat_session_id=model.chat_session_id, created_at=model.created_at, updated_at=model.updated_at)
    def to_socket_message(self):
        from helpr.socket_components.message import SocketServerMessageBotChat
        return SocketServerMessageBotChat(message=self)

class SystemMessageSchema(MessageSchema):
    type: str = MessageSchema.Type.SYSTEM_MESSAGE
    def from_model(model: DBSystemMessage):
          return SystemMessageSchema(id=model.id, text=model.text, chat_session_id=model.chat_session_id, created_at=model.created_at, updated_at=model.updated_at)
      

class ActionRequestMessageSchema(MessageSchema):
    action_request_id: int
    action_request: Optional[ActionRequestSchema]
    type: str = MessageSchema.Type.ACTION_REQUEST_MESSAGE
    def from_model(model: DBActionRequestMessage):
          return ActionRequestMessageSchema(id=model.id, chat_session_id=model.chat_session_id, action_request_id=model.action_request_id, action_request=ActionRequestSchema.from_model(model.action_request) if model.action_request else None, text=None, created_at=model.created_at, updated_at=model.updated_at)
    def to_socket_message(self):
        from helpr.socket_components.message import SocketServerMessageActionRequestChat
        return SocketServerMessageActionRequestChat(message=self)

      
#TODO: should store input aswell right?
class ActionResultMessageSchema(MessageSchema):
    action_id: int
    action: Optional[ActionSchema]
    output: str
    type: str = MessageSchema.Type.ACTION_RESULT_MESSAGE
    def from_model(model: DBActionResultMessage):
          return ActionResultMessageSchema(id=model.id, chat_session_id=model.chat_session_id, created_at=model.created_at, updated_at=model.updated_at, action_id=model.action_id, output=model.output, text=model.text, action=ActionSchema.from_model(model.action) if model.action else None)
    def to_socket_message(self):
        from helpr.socket_components.message import SocketServerMessageActionResultChat
        return SocketServerMessageActionResultChat(message=self)

"""
class ActionRequestResponseMessageSchema(MessageSchema):
    request_message_id: int
    feedback: Optional[str] = None
    approved: bool
    type: str = MessageSchema.Type.ACTION_REQUEST_RESPONSE_MESSAGE
    def from_model(model: DBActionRequestResponseMessage):
          return ActionRequestResponseMessageSchema(id=model.id, text=model.text, chat_session_id=model.chat_session_id, created_at=model.created_at, updated_at=model.updated_at, request_message_id=model.request_message_id, feedback=model.feedback, approved=model.approved)
    def to_socket_message(self):
        from helpr.socket_components.message import SocketServerMessageActionRequestResponseChat
        return SocketServerMessageActionRequestResponseChat(message=self)
"""

class UserMessageSchema(MessageSchema):
    text: str
    type: str = MessageSchema.Type.USER_MESSAGE
    def from_model(model: DBBotMessage):
        return UserMessageSchema(id=model.id, text=model.text, chat_session_id=model.chat_session_id, created_at=model.created_at, updated_at=model.updated_at)
