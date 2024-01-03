from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from click import Option
from pydantic import BaseModel
from helpr.db.models.message import DBActionRequestMessage, DBBotMessage, DBMessage, DBActionRequestResponseMessage, DBSystemMessage, DBActionResultMessage
from helpr.socket_components.message import SocketServerMessageActionRequestChat, SocketServerMessageActionResultChat, SocketServerMessageBotChat
from helpr.schemas.action import ActionSchema
from sqlalchemy.orm import make_transient, make_transient_to_detached
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


class dto:
    class CreateMessage(BaseModel):
        text: Optional[str] = None
        chat_session_id: int

    class CreateBotMessage(CreateMessage):
        pass

    class CreateUserMessage(CreateMessage):
        pass
    
    class CreateActionRequestMessage(CreateMessage):
        input: str
        action_id: int
        
    class CreateActionResultMessage(CreateMessage):
        output: str
        action_id: int
        
    class CreateActionRequestResponseMessage(CreateMessage):
        feedback: str
        approved: bool
        request_message_id: int


class BotMessageSchema(MessageSchema):
    text: str
    type: str = MessageSchema.Type.BOT_MESSAGE
    def from_model(model: DBBotMessage):
        return BotMessageSchema(id=model.id, text=model.text, chat_session_id=model.chat_session_id, created_at=model.created_at, updated_at=model.updated_at)
    def to_socket_message(self):
        return SocketServerMessageBotChat(chat_session_id=self.chat_session_id, text=self.text)

class SystemMessageSchema(MessageSchema):
    type: str = MessageSchema.Type.SYSTEM_MESSAGE
    def from_model(model: DBSystemMessage):
          return SystemMessageSchema(id=model.id, text=model.text, chat_session_id=model.chat_session_id, created_at=model.created_at, updated_at=model.updated_at)
      

class ActionRequestMessageSchema(MessageSchema):
    action_id: int
    action: Optional[ActionSchema]
    input: str
    type: str = MessageSchema.Type.ACTION_REQUEST_MESSAGE
    def from_model(model: DBActionRequestMessage):
          return ActionRequestMessageSchema(id=model.id, text=model.text, chat_session_id=model.chat_session_id, created_at=model.created_at, updated_at=model.updated_at, action_id=model.action_id, input=model.input, action=ActionSchema.from_model(model.action) if model.action else None)
    def to_socket_message(self):
        return SocketServerMessageActionRequestChat(chat_session_id=self.chat_session_id, text=self.text, input=str(self.input), action_id=self.action_id)

      
#TODO: should store input aswell right?
class ActionResultMessageSchema(MessageSchema):
    action_id: int
    action: Optional[ActionSchema]
    output: str
    type: str = MessageSchema.Type.ACTION_RESULT_MESSAGE
    def from_model(model: DBActionResultMessage):
          return ActionResultMessageSchema(id=model.id, chat_session_id=model.chat_session_id, created_at=model.created_at, updated_at=model.updated_at, action_id=model.action_id, output=model.output, text=model.text, action=ActionSchema.from_model(model.action) if model.action else None)
    def to_socket_message(self):
        return SocketServerMessageActionResultChat(chat_session_id=self.chat_session_id, text=self.text, action_id=self.action_id, output=self.output)


class ActionRequestResponseMessageSchema(MessageSchema):
    request_message_id: int
    feedback: Optional[str] = None
    approved: bool
    type: str = MessageSchema.Type.ACTION_REQUEST_RESPONSE_MESSAGE
    def from_model(model: DBActionRequestResponseMessage):
          return ActionRequestResponseMessageSchema(id=model.id, text=model.text, chat_session_id=model.chat_session_id, created_at=model.created_at, updated_at=model.updated_at, request_message_id=model.request_message_id, feedback=model.feedback, approved=model.approved)


class UserMessageSchema(MessageSchema):
    text: str
    type: str = MessageSchema.Type.USER_MESSAGE
    def from_model(model: DBBotMessage):
        return UserMessageSchema(id=model.id, text=model.text, chat_session_id=model.chat_session_id, created_at=model.created_at, updated_at=model.updated_at)
