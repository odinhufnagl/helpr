from typing import List, Literal, Optional
from click import Option
from numpy import isin
from pydantic import BaseModel
from db.models.agent import DBAgent
from db.models.index import DBIndex
from helpr.action.action_registry import ActionRegistry
from helpr.action.base import AddAction, BaseAction, PrintAction
from helpr.config.ai_config import AIConfig
from helpr.prompt_generator.base import PromptGenerator
from helpr.services.action import get_actions_in_chat
from index.base import Index
from llama_index.llms.types import ChatMessage, MessageRole
from index.location import BaseIndexLocation, IndexLocationDir
from llama_index.tools import ToolOutput
import db
from db.models import DBChatSession, DBChat
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from schemas.message import ActionRequestMessageSchema, ActionResultMessageSchema, BotMessageSchema, MessageSchema, UserMessageSchema
import services.message as message_service
import services.action_request as action_request_service
from schemas.message import dto as message_dto
from schemas.action_request import dto as action_request_dto
from llama_index.chat_engine.types import AGENT_CHAT_RESPONSE_TYPE
from llama_index.tools import FunctionTool



class MessageCollection(BaseModel):
    chat_session_id: int
    offset: int = 0
    limit: int = 10
    order: Literal['desc', 'asc']
    messages: List[MessageSchema] = []
    
    def get_messages(self):
        return self.messages

    async def fetch_next(self):
        # TODO: check the ordering here
        new_messages, count = (await message_service.get_messages(self.chat_session_id, order=self.order, limit=self.limit, offset=self.offset))
        new_messages = new_messages[::-1]
        new_offset = self.offset + self.limit
        self.offset = new_offset
        # TODO: check the ordering here
        self.messages = self.messages + new_messages
        return self.messages

    async def add_bot_message(self, message_schema: message_dto.CreateBotMessage) -> BotMessageSchema:
        created_message = await message_service.create_bot_message(message_schema)
        self.messages.append(created_message)
        return created_message

    async def add_action_request_message(self, chat_session_id: int, action_request: action_request_dto.CreateActionRequest) -> ActionRequestMessageSchema:
        created_action_request = await action_request_service.create_request(action_request)
        created_message = await message_service.create_action_request_message(message_dto.CreateActionRequestMessage(chat_session_id=chat_session_id, action_request_id=created_action_request.id))
        self.messages.append(created_message)
        return created_message

    async def add_action_result_message(self, message_schema: message_dto.CreateActionResultMessage) -> ActionResultMessageSchema:
        created_message = await message_service.create_action_result_message(message_schema)
        self.messages.append(created_message)
        return created_message