

from typing import List, Literal
from helpr import db
from helpr.db.models.action import DBAction, DBAddAction, DBPostRequestAction
from helpr.db.models.chat import DBChat
from helpr.db.models.chat_action import DBChatAction
from helpr.schemas.action import ActionSchema
from sqlalchemy import select
from sqlalchemy.orm import with_polymorphic, selectin_polymorphic,joinedload
from helpr.logger import logger

async def get_actions_in_chat(chat_id: int) -> List[ActionSchema]:
    async with db.session() as session:
        actions = (await session.execute(
            select(DBAction).options(selectin_polymorphic(DBAction, [DBAddAction, DBPostRequestAction])).options(joinedload(DBPostRequestAction.headers_field), joinedload(DBPostRequestAction.url_field)).join(DBChatAction).filter( #TODO: joinedload('*') bad
                DBChatAction.chat_id == chat_id)
        )).unique().scalars().all()
        await session.commit()
    logger.info(f"actions: {actions}")
    return list(map(lambda m: ActionSchema.from_model(m), actions))