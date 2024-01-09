from cmath import e
from email.errors import MessageError
from re import S
import string
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
from helpr.schemas.action_request import ActionRequestResponseSchema, ActionRequestSchema
from helpr.schemas.action_run import ActionRunSchema
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

class ChatAgentMessage(BaseModel):

    class Config:
        arbitrary_types_allowed = True

    # TODO: add the rest

    @staticmethod
    def from_schema(schema: MessageSchema) -> 'ChatAgentMessage':
        if isinstance(schema, BotMessageSchema):
            return BotChatAgentMessage(text=schema.text)
        if isinstance(schema, UserMessageSchema):
            return UserChatAgentMessage(text=schema.text)
        if isinstance(schema, ActionRequestMessageSchema):
            return ActionRequestAgentMessage.from_action_request_schema(schema.action_request)
        if isinstance(schema, ActionResultMessageSchema):
            return ActionResultMessage(output=schema.output, action=BaseAction.from_schema(schema.action))
        """  if isinstance(schema, ActionRequestResponseMessageSchema):
            return ActionRequestResponseAgentMessage(approved=schema.approved, feedback=schema.feedback, action_request_id=schema.request_message_id)
        """

    @staticmethod
    def from_schemas(schemas: List[MessageSchema]):
        return list(map(lambda s: ChatAgentMessage.from_schema(s), schemas))


class UserChatAgentMessage(ChatAgentMessage):

    text: str


class SystemChatAgentMessage(ChatAgentMessage):

    text: str


class BotChatAgentMessage(ChatAgentMessage):

    text: str


class ActionRequestAgentMessage(ChatAgentMessage):
    class Config:
        arbitrary_types_allowed = True
    text: Optional[str]
    action: Optional[BaseAction]
    input: BaseAction.Input | str  # TODO: should not be allowed to be str
    response: Optional['ActionRequestResponseAgentMessage'] = None

    def from_action_request_schema(schema: ActionRequestSchema):
        return ActionRequestAgentMessage(text=None, action=BaseAction.from_schema(schema.action), input=schema.input, response=ActionRequestResponseAgentMessage.from_action_request_response_schema(schema.response) if schema.response else None)


class ActionRequestResponseAgentMessage(ChatAgentMessage):
    feedback: Optional[str] = None
    approved: bool
    action_result: Optional['ActionResultMessage'] = None
    next_action_request: Optional['ActionRequestAgentMessage'] = None

    def from_action_request_response_schema(schema: ActionRequestResponseSchema):
        return ActionRequestResponseAgentMessage(action_result=ActionResultMessage.from_action_run_schema(schema.action_run) if schema.action_run else None, approved=schema.approved, feedback=schema.feedback, next_action_request=ChatAgentMessage.from_schema(schema.next_action_request) if schema.next_action_request else None)


class ActionResultMessage(ChatAgentMessage):
    output: BaseAction.Output | str  # TODO: should not be allowed to be str
    action: Optional[BaseAction]

    def from_action_run_schema(schema: ActionRunSchema):
        return ActionResultMessage(output=schema.output, action=BaseAction.from_schema(schema.action))


class ActionResultSummaryMessage(ChatAgentMessage):

    action_result: ActionResultMessage
    text: str


class ChatEngineMessage(ChatMessage):
    @staticmethod
    def from_chat_message(msg: ChatAgentMessage):
        if isinstance(msg, UserChatAgentMessage):
            return ChatEngineMessage(role=MessageRole.USER, content=msg.text)
        if isinstance(msg, BotChatAgentMessage):
            return ChatEngineMessage(role=MessageRole.ASSISTANT, content=msg.text)
        if isinstance(msg, SystemChatAgentMessage):
            return ChatEngineMessage(role=MessageRole.SYSTEM, content=msg.text)
        if isinstance(msg, ActionRequestAgentMessage):
            # TODO: this should also be done with some generator
            # TODO: should say action.name
            return ChatEngineMessage(role=MessageRole.ASSISTANT, content=f"text: {msg.text}, function: {msg.action} with input: {msg.input}")
        if isinstance(msg, ActionRequestResponseAgentMessage):
            # TODO: for example this should match how the text looks when we put it as input_text so it should come from same generator
            if msg.feedback:
                # TODO: this must probably be changed so it is connected to the action_request
                return ChatEngineMessage(role=MessageRole.USER, content=f'feedback: {msg.feedback} to the action')
            if msg.approved:
                return ChatEngineMessage(role=MessageRole.USER, content=f'I approve of the action')
            if not msg.approved:
                return ChatEngineMessage(role=MessageRole.USER, content=f'I do not approve the action')
        if isinstance(msg, ActionResultMessage):
            # TODO: should function response come from system?
            # TODO: should say action.name
            return ChatEngineMessage(role=MessageRole.ASSISTANT, content=f'result: {msg.output} to action: {msg.action}')
        if isinstance(msg, ActionResultSummaryMessage):
            return ChatEngineMessage(role=MessageRole.SYSTEM, content=msg.text)

    def from_chat_messages(messages: List[ChatAgentMessage]) -> List['ChatEngineMessage']:
        engine_messages: List[ChatEngineMessage] = []
        for message in messages:
            if isinstance(message, ActionRequestAgentMessage):
                engine_messages.append(ChatEngineMessage.from_chat_message(message))
                if message.response:
                    engine_messages.append(ChatEngineMessage.from_chat_message(message.response))
            else:
                engine_messages.append(ChatEngineMessage.from_chat_message(message))
        return engine_messages

class ChatAgent:

    def __init__(self, index: Index, prompt: str, message_history: List[ChatAgentMessage], action_registry: ActionRegistry) -> None:
        self.index = index
        # TODO: if this ChatAgent should be able to have its own implementations so its quite modular, it shuoldnt take in the prompt right? Because the prompt
        # might be different for another chat_agent, and right now we have tried to make the messages as abstract as possible (not linked to the logic of the chat-function)
        # Or maybe just switch lane and build everything with the idea that we are using llama. Maybe not the best best, but will improve the flow in some ways
        self.prompt = prompt
        self.message_history = message_history
        self.action_registry = action_registry

    # TODO: put in utils?
    @staticmethod
    def actions_to_tools(actions: List[BaseAction]):
        tools = []
        for action in actions:
            if action.feedback_required:

                tool = FunctionTool.from_defaults(
                    fn=action.empty_run, description=action.description, name=action.name)
            else:
                tool = FunctionTool.from_defaults(
                    fn=action.run, description=action.description, name=action.name)
            tools.append(tool)
        return tools

    def parse_chat_response(self, response: AGENT_CHAT_RESPONSE_TYPE) -> List[ChatAgentMessage]:
        responses = []
        sources = response.sources
        for source in sources:
            if isinstance(source, ToolOutput):
                action = self.action_registry.get(source.tool_name)
                k = source.raw_input['kwargs']
                i = action.Input(**k)
                if not action:
                    return responses
                if action.feedback_required:  # TODO: check that the action is feedback_required
                    message = ActionRequestAgentMessage(
                        text=response.response, action=action,  input=i)
                    responses.append(message)  # TODO: better input parsing
                    return responses
                else:
                    print("raw_output", source.raw_output)
                    responses.append(ActionResultMessage(
                        action=action, output=source.raw_output))
        responses.append(BotChatAgentMessage(text=response.response))

        return responses
    
    
    async def chat(self) -> List[ChatAgentMessage]:
        created_messages: List[ChatAgentMessage] = []
        if len(self.message_history) == 0:
            return
        print("message_history", self.message_history)
        chat_history = ChatEngineMessage.from_chat_messages(
            self.message_history)
        latest_message = chat_history[-1]
        rest_of_messages = chat_history[:-1]
        tools = self.actions_to_tools(
            self.action_registry.actions)  # TODO: ugly
        chat_engine = self.index.as_chat_engine(
            system_prompt=self.prompt, tools=tools)
        print("chat_history", chat_history)
        if latest_message.role != MessageRole.ASSISTANT:
            input_text = latest_message.content
            response = chat_engine.chat(input_text, chat_history=rest_of_messages)
            new_messages = self.parse_chat_response(response)
            created_messages += new_messages
            self.message_history += created_messages

            return created_messages
        else:
            return []
       
        # TODO: ignoring symmary of action for now
        """   if isinstance(latest_message, ActionResultMessage):
        # TODO: same as above, should come from some generator
        input_text = f"Action {latest_message.action.name} returned {latest_message.output.dict()}. Summary this result"
        response = chat_engine.chat(input_text, chat_history=chat_history)
        (text, action, args) = self.parse_chat_response(response)
        created_messages.append(ActionResultSummaryMessage(
            text=text, action_result=latest_message))"""



    def update_message_history(self, new_message_history):
        self.message_history = new_message_history


class MessageSchemaCollection(BaseModel):
    chat_session_id: int
    offset: int = 0
    limit: int = 10
    order: Literal['desc', 'asc']
    messages: List[MessageSchema] = []

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


# TODO: look over db structure, because this requires action-name to be unique which OBVIOUSLY is wrong. Or maybe not obvious but something has to change, perhaps the "name" of the action in the tools should be the id or something like that
async def get_action_by_name_in_db(action_name: str) -> db.models.DBAction:
    async with db.session() as session:
        m = (await session.execute(select(db.models.DBAction).where(db.models.DBAction.name == action_name))).scalar_one_or_none()
        await session.commit()
    return m


class ChatSessionAgent(BaseModel):

    class Config:
        arbitrary_types_allowed = True

    organization_id: int
    chat_session_id: int
    agent: ChatAgent
    message_collection: MessageSchemaCollection

    # TODO: lots of the code here should go to other modules, there are way too much possible complexity here

    async def chat(self) -> List[MessageSchema]:
        self.agent.update_message_history(
            ChatAgentMessage.from_schemas(self.message_collection.messages))
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
                created_message = await self.message_collection.add_action_request_message(self.chat_session_id, action_request_dto.CreateActionRequest(action_id=db_action.id, input=msg.input.__str__(), response_id=None, action_run_id=None))
                created_messages.append(created_message)
            if isinstance(msg, ActionResultMessage):
                # TODO: will change
                db_action = await get_action_by_name_in_db(msg.action.name)

                # TODO: fix action_id
                created_message = await self.message_collection.add_action_result_message(message_dto.CreateActionResultMessage(text='', chat_session_id=self.chat_session_id, action_id=db_action.id, output=msg.output.__str__()))
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
        message_collection = MessageSchemaCollection(
            chat_session_id=chat_session_id, limit=20, order='desc')
        await message_collection.fetch_next()
        message_history = ChatAgentMessage.from_schemas(
            message_collection.messages)
        chat_agent = ChatAgent(prompt=prompt, index=index,
                               message_history=message_history, action_registry=action_registry)

        new_session_agent = ChatSessionAgent(chat_session_id=chat_session_id, organization_id=db_chat.organization_id,
                                             agent=chat_agent, message_collection=message_collection)
        return new_session_agent
