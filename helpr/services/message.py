
import copy
from typing import List, Literal

from helpr import db
from helpr.db.models.action import DBAction, DBAddAction, DBPostRequestAction
from helpr.db.models.action_request import DBActionRequest, DBActionRequestResponse
from helpr.db.models.message import DBActionRequestMessage, DBActionResultMessage, DBMessage, DBBotMessage, DBUserMessage
from schemas.message import ActionResultMessageSchema, BotMessageSchema, MessageSchema, dto, BaseSchema, UserMessageSchema
from sqlalchemy import func, select
from sqlalchemy.orm import with_polymorphic, joinedload, selectin_polymorphic, selectinload, make_transient
from helpr.logger import logger


async def create(data: dto.CreateMessage) -> MessageSchema:
    async with db.session() as session:
        m = DBMessage(chat_session_id=data.chat_session_id, text=data.text)
        session.add(m)
        await session.commit()
    return MessageSchema.from_model(m)


async def create_bot_message(data: dto.CreateBotMessage) -> BotMessageSchema:
    async with db.session() as session:
        m = DBBotMessage(chat_session_id=data.chat_session_id, text=data.text)
        session.add(m)
        await session.commit()
    return MessageSchema.from_model(m)


async def create_action_request_message(data: dto.CreateActionRequestMessage) -> BotMessageSchema:
    async with db.session() as session:
        m = DBActionRequestMessage(
            text=data.text if data.text else '',
            chat_session_id=data.chat_session_id, action_request_id=data.action_request_id)
        session.add(m)
        await session.commit()
    return MessageSchema.from_model(m)


async def create_action_result_message(data: dto.CreateActionResultMessage) -> ActionResultMessageSchema:
    async with db.session() as session:
        m = DBActionResultMessage(chat_session_id=data.chat_session_id,
                                  text=data.text if data.text else '', action_id=data.action_id, output=data.output)
        session.add(m)
        await session.commit()
    return MessageSchema.from_model(m)

"""async def create_action_request_response_message(data: dto.CreateActionRequestResponseMessage) -> BotMessageSchema:
    async with db.session() as session:
        m = DBActionRequestResponseMessage(chat_session_id=data.chat_session_id, text='', approved=data.approved, feedback=data.feedback, request_message_id=data.request_message_id)
        session.add(m)
        await session.commit()"""


async def create_user_message(data: dto.CreateUserMessage) -> UserMessageSchema:
    async with db.session() as session:
        m = DBUserMessage(chat_session_id=data.chat_session_id, text=data.text)
        session.add(m)
        await session.commit()
    return MessageSchema.from_model(m)


async def get_message_by_id(id: int) -> MessageSchema:
    async with db.session() as session:
        # TODO: simplify and centralize pagination
        message_query = (select(DBMessage).options(selectin_polymorphic(DBMessage, [DBBotMessage, DBUserMessage, DBActionRequestMessage, DBActionResultMessage]), selectinload(DBActionResultMessage.action).options(selectin_polymorphic(DBAction, [DBAddAction, DBPostRequestAction])).options(joinedload(DBPostRequestAction.headers_field), joinedload(DBPostRequestAction.url_field)), joinedload(DBActionRequestMessage.action_request).joinedload(DBActionRequest.action).options(selectin_polymorphic(DBAction, [DBAddAction, DBPostRequestAction])).options(joinedload(DBPostRequestAction.headers_field), joinedload(DBPostRequestAction.url_field)), joinedload(DBActionRequestMessage.action_request).joinedload(
            DBActionRequest.response).joinedload(DBActionRequestResponse.action_run)).where(DBMessage.id == id))
        m = (await session.execute(message_query)).scalar_one_or_none()
        await session.commit()
    return MessageSchema.from_model(m)
 

async def get_messages(chat_session_id: int, offset: int = 0, limit: int = 100, order: Literal['desc', 'asc'] = 'asc') -> tuple[List[MessageSchema], int]:
    async with db.session() as session:
        print("limit", limit, offset)
        # TODO: simplify and centralize pagination
        message_query = (select(DBMessage).options(selectin_polymorphic(DBMessage, [DBBotMessage, DBUserMessage, DBActionRequestMessage, DBActionResultMessage]), selectinload(DBActionResultMessage.action).options(selectin_polymorphic(DBAction, [DBAddAction, DBPostRequestAction])).options(joinedload(DBPostRequestAction.headers_field), joinedload(DBPostRequestAction.url_field)), joinedload(DBActionRequestMessage.action_request).joinedload(DBActionRequest.action).options(selectin_polymorphic(DBAction, [DBAddAction, DBPostRequestAction])).options(joinedload(DBPostRequestAction.headers_field), joinedload(DBPostRequestAction.url_field)), joinedload(DBActionRequestMessage.action_request).joinedload(
            DBActionRequest.response).joinedload(DBActionRequestResponse.action_run)).where(DBMessage.chat_session_id == chat_session_id).order_by(DBMessage.created_at.desc() if order == 'desc' else DBMessage.created_at.asc()).offset(offset).limit(limit))
        count_query = select(func.count()).select_from(
            message_query.subquery())
        count = (await session.execute(count_query)).scalar()
        messages = (await session.execute(message_query)).scalars().all()
        await session.commit()
    return list(map(lambda m: MessageSchema.from_model(m), messages)), count
