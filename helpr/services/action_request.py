from helpr.schemas.action_request import ActionRequestResponseSchema, ActionRequestSchema, dto
import copy
from typing import List, Literal
from helpr import db
from helpr.db.models.action_request import DBActionRequest, DBActionRequestResponse
from helpr.services.database import update


async def create_request(data: dto.CreateActionRequest) -> ActionRequestSchema:
    async with db.session() as session:
        m = DBActionRequest(**data.__dict__)
        session.add(m)
        await session.commit()
    return ActionRequestSchema.from_model(m)



async def create_response(data: dto.CreateActionResponse) -> ActionRequestResponseSchema:
    async with db.session() as session:
        m = DBActionRequestResponse(**data.__dict__)
        session.add(m)
        await session.commit()
        await update(DBActionRequest, m.action_request_id, {'response_id': m.id})
        await session.commit()

    return ActionRequestResponseSchema.from_model(m)

