

from typing import List, Literal
from helpr import db
from helpr.db.models.action import DBAction, DBAddAction, DBPostRequestAction
from helpr.db.models.action_request import DBActionRequest, DBActionRequestResponse
from helpr.db.models.action_run import DBActionRun
from sqlalchemy import select
from sqlalchemy.orm import with_polymorphic, selectin_polymorphic,joinedload
from helpr.logger import logger
from helpr.schemas.action_run import ActionRunSchema
from helpr.services.database import get
from helpr.action.base import BaseAction
from helpr.db.models.action_run import DBActionRun
from helpr.schemas.action_run import ActionRunSchema
from helpr.services.database import update
from schemas.action_run import dto



async def get_action_run_by_id(id: int) -> ActionRunSchema:
    async with db.session() as session:
        # TODO: simplify and centralize pagination
        message_query = (select(DBActionRun).where(DBActionRun.id == id).options(joinedload(DBActionRun.action).options(selectin_polymorphic(DBAction, [DBAddAction, DBPostRequestAction])).options(joinedload(DBPostRequestAction.headers_field), joinedload(DBPostRequestAction.url_field))))
        m = (await session.execute(message_query)).scalar_one_or_none()
        await session.commit()
    return ActionRunSchema.from_model(m)
    
async def create(data: dto.CreateActionRun) -> ActionRunSchema:
    async with db.session() as session:
        m = DBActionRun(**data.__dict__)
        session.add(m)
        await session.commit()
    return ActionRunSchema.from_model(m)
