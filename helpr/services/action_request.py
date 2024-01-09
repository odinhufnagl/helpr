from venv import logger
from helpr.schemas import action
from helpr.schemas.action_request import ActionRequestResponseSchema, ActionRequestSchema, dto
import copy
from typing import List, Literal
from helpr import db
from helpr.db.models.action_request import DBActionRequest, DBActionRequestResponse
from helpr.services.database import get, update


async def create_request(data: dto.CreateActionRequest) -> ActionRequestSchema:
    async with db.session() as session:
        m = DBActionRequest(**data.__dict__)
        session.add(m)
        await session.commit()
    return ActionRequestSchema.from_model(m)

async def request_has_response(request_id) -> bool:
    action_request = await get(DBActionRequest, request_id)
    logger.info(f"action_request: {action_request}")
    if action_request.response_id == None:
        return False
    return True

async def create_new_response(data: dto.CreateActionResponse) -> ActionRequestResponseSchema | None:
    async with db.session() as session:
        if await request_has_response(data.action_request_id):
            return None
        m = DBActionRequestResponse(**data.__dict__)
        session.add(m)
        await session.commit()
        await update(DBActionRequest, m.action_request_id, {'response_id': m.id})
        await session.commit()

    return ActionRequestResponseSchema.from_model(m)

