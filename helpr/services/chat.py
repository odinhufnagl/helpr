

from helpr import db
from helpr.db.models.chat import DBChat
from helpr.db.models.message import DBMessage
from schemas.chat import ChatSchema, dto


async def create(data: dto.CreateChat) -> ChatSchema:
    async with db.session() as session:
        m = DBChat(agent_id=data.agent_id, organization_id=data.organization_id,
                   name=data.name, system_prompt=data.system_prompt)
        session.add(m)
        await session.commit()
    return ChatSchema.from_model(m)
