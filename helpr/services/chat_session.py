from sqlalchemy import select
from helpr import db
from helpr.db.models.chat import DBChat
from helpr.db.models.chat_session import DBChatSession
from helpr.db.models.message import DBMessage
from helpr.schemas.chat_session import ChatSessionSchema
from schemas.chat import ChatSchema, dto


async def create(chat_id: int) -> ChatSchema:
    async with db.session() as session:
        model = db.models.DBChatSession(chat_id=chat_id)
        session.add(model)
        await session.commit()
    return ChatSessionSchema.from_model(model)

async def get(id: int) -> ChatSessionSchema:
    async with db.session() as session:
        model = (await session.execute(select(DBChatSession).where(DBChatSession.id == id))).scalar_one_or_none()
        await session.commit()
    return ChatSessionSchema.from_model(model)