

from helpr import db
from helpr.db.models.message import DBMessage
from schemas.message import MessageSchema, dto, BaseSchema


async def create(data: dto.CreateMessage) -> MessageSchema:
  async with db.session() as session:
      m = DBMessage(chat_session_id=data.chat_session_id, text=data.text)
      session.add(m)
      await session.commit()
  return MessageSchema.from_model(m)

