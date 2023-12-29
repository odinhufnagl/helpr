
import copy
from typing import List, Literal

from helpr import db
from helpr.db.models.message import DBActionRequestMessage, DBActionRequestResponseMessage, DBActionResultMessage, DBMessage, DBBotMessage, DBUserMessage
from schemas.message import BotMessageSchema, MessageSchema, dto, BaseSchema, UserMessageSchema
from sqlalchemy import select
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
        m = DBActionRequestMessage(chat_session_id=data.chat_session_id, text=data.text, action_id=data.action_id, input=data.input)
        session.add(m)
        await session.commit()
    return MessageSchema.from_model(m)


async def create_action_result_message(data: dto.CreateActionResultMessage) -> BotMessageSchema:
    async with db.session() as session:
        m = DBActionResultMessage(chat_session_id=data.chat_session_id, text=data.text, action_id=data.action_id, output=data.output)
        session.add(m)
        await session.commit()
    return MessageSchema.from_model(m)

async def create_action_request_response_message(data: dto.CreateActionRequestResponseMessage) -> BotMessageSchema:
    async with db.session() as session:
        m = DBActionRequestResponseMessage(chat_session_id=data.chat_session_id, text=data.text, approved=data.approved, feedback=data.feedback, request_message_id=data.request_message_id)
        session.add(m)
        await session.commit()

async def create_user_message(data: dto.CreateUserMessage) -> UserMessageSchema:
    async with db.session() as session:
        m = DBUserMessage(chat_session_id=data.chat_session_id, text=data.text)
        session.add(m)
        await session.commit()
    return MessageSchema.from_model(m)

async def get_messages(chat_session_id: int, offset: int = 0, limit: int = 100, order: Literal['desc', 'asc'] = 'asc') -> List[MessageSchema]:
    async with db.session() as session:
        messages = (await session.execute(select(DBMessage).options(selectin_polymorphic(DBMessage, [DBBotMessage, DBUserMessage, DBActionRequestMessage, DBActionRequestResponseMessage, DBActionResultMessage]), selectinload(DBActionResultMessage.action), selectinload(DBActionRequestMessage.action)).where(DBMessage.chat_session_id == chat_session_id).order_by(DBMessage.created_at.desc() if order == 'desc' else DBMessage.created_at.asc()).offset(offset).limit(limit))).scalars().all()

    return list(map(lambda m: MessageSchema.from_model(m), messages))   
    