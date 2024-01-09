from typing import List, Literal, Optional
from numpy import isin
from pydantic import BaseModel
from db.models.agent import DBAgent
from db.models.index import DBIndex
from helpr.action.action_registry import ActionRegistry
from helpr.action.base import AddAction, BaseAction, PrintAction
from helpr.agent.chat_agent import ChatAgent
from helpr.config.ai_config import AIConfig
from helpr.messages.message_collection import MessageCollection
from helpr.prompt_generator.base import PromptGenerator
from helpr.utils.convert import base_model_to_json
from .chat_agent_message import *
from helpr.services.action import get_action_by_name_in_db, get_actions_in_chat
from index.base import Index
from llama_index.llms.types import ChatMessage, MessageRole
from index.location import BaseIndexLocation, IndexLocationDir
import db
from db.models import DBChatSession, DBChat
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from schemas.message import MessageSchema
import services.message as message_service
import services.action_request as action_request_service
from schemas.message import dto as message_dto
from schemas.action_request import dto as action_request_dto
from llama_index.chat_engine.types import AGENT_CHAT_RESPONSE_TYPE
from llama_index.tools import FunctionTool

class ChatSessionAgent(BaseModel):

    class Config:
        arbitrary_types_allowed = True

    organization_id: int
    chat_session_id: int
    agent: ChatAgent
    message_collection: MessageCollection

    # TODO: lots of the code here should go to other modules, there are way too much possible complexity here

    async def chat(self) -> List[MessageSchema]:
        self.agent.update_message_history(
            ChatAgentMessage.from_schemas(self.message_collection.get_messages()))
        chat_response = await self.agent.chat()
        created_messages = []
        for msg in chat_response:
            # TODO: take into account all types of ChatAgentMessages, also this looks ugly here
            if isinstance(msg, BotChatAgentMessage):
                created_message = await self.message_collection.add_bot_message(message_dto.CreateBotMessage(text=msg.text, chat_session_id=self.chat_session_id))
                created_messages.append(created_message)
            if isinstance(msg, ActionRequestAgentMessage):

                # TODO: will change
                db_action = await get_action_by_name_in_db(msg.action.name)
                # TODO: text should be able to be None
                # TODO: fix action_id
                created_message = await self.message_collection.add_action_request_message(self.chat_session_id, action_request_dto.CreateActionRequest(action_id=db_action.id, input=base_model_to_json(msg.input), response_id=None, action_run_id=None))
                created_messages.append(created_message)
            if isinstance(msg, ActionResultMessage):
                # TODO: will change
                db_action = await get_action_by_name_in_db(msg.action.name)

                # TODO: fix action_id
                created_message = await self.message_collection.add_action_result_message(message_dto.CreateActionResultMessage(text='', chat_session_id=self.chat_session_id, action_id=db_action.id, output=base_model_to_json(msg.output)))
                created_messages.append(created_message)
            else:
                pass
                # TODO: add functionrequest message if that is needed
                # TODO: else start the task
                #  created_message = await self.message_collection.add_
        #TODO: just temporary to return them fully extended

        return [await message_service.get_message_by_id(x.id) for x in created_messages]

    @staticmethod
    async def construct_default(chat_session_id: int) -> Optional['ChatSessionAgent']:
        async with db.session() as session:
            chat_session = (await session.execute(select(DBChatSession).where(DBChatSession.id == chat_session_id).options(selectinload(DBChatSession.chat).options(selectinload(DBChat.agent).options(selectinload(DBAgent.index)))))).scalar_one_or_none()
            await session.commit()
        if not chat_session.chat.agent.index:
            return None
        db_chat: DBChat = chat_session.chat
        db_agent: DBAgent = chat_session.chat.agent
        db_index: DBIndex = db_agent.index
        action_schemas = await get_actions_in_chat(db_chat.id)
        action_registry = ActionRegistry()
        for schema in action_schemas:
            action_registry.register_schema(schema)

        prompt_generator = PromptGenerator(action_registry=action_registry)
        prompt_generator.set_context(db_chat.system_prompt)
        ai_config = AIConfig()
        # TODO: just temporary
        index_location = IndexLocationDir.from_db_index_location(
            db_index=db_index.location)
        index = index_location.load_index(db_index.id)
        prompt = ai_config.construct_full_prompt(prompt_generator)
        message_collection = MessageCollection(
            chat_session_id=chat_session_id, limit=20, order='desc')
        await message_collection.fetch_next()
        message_history = ChatAgentMessage.from_schemas(
            message_collection.get_messages())
        chat_agent = ChatAgent(prompt=prompt, index=index,
                               message_history=message_history, action_registry=action_registry)

        new_session_agent = ChatSessionAgent(chat_session_id=chat_session_id, organization_id=db_chat.organization_id,
                                             agent=chat_agent, message_collection=message_collection)
        return new_session_agent
