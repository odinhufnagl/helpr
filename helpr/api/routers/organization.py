from typing import List
from fastapi import APIRouter, Depends, Request
from helpr.logger import logger
from pydantic import BaseModel
from sqlalchemy import select
import db
from helpr.api.middleware.auth import PermissionChecker
from helpr.api.request.base import AuthedRequest
from helpr.organizations.permissions import Permission, PermissionRole
from helpr.schemas import OrganizationSchema
import helpr.services.chat as chat_service

router = APIRouter(prefix='/organizations')


def permission_check_with_path_id(allowed_roles: List[PermissionRole] = [], allowed_permissions: List[Permission] = []):
    async def f(request: Request, organization_id: int):
        request = AuthedRequest.from_request(request)
        return await PermissionChecker(allowed_roles=allowed_roles, allowed_permissions=allowed_permissions)(request.user_id, organization_id)
    return f

@router.get('/{organization_id}')
async def get_organization(organization_id: int, has_access = Depends(permission_check_with_path_id(allowed_roles=['admin']))):
    async with db.session() as session:
        model = (await session.execute(select(db.models.DBOrganization).where(db.models.DBOrganization.id == organization_id))).scalar_one_or_none()
        await session.commit()
    #TODO: should be classes for response
    return OrganizationSchema.from_model(model)

class PostChat(BaseModel):
    agent_id: int
    name: str
    system_prompt: str

@router.post("/{organization_id}/chat")
async def post_chat(organization_id: int, params: PostChat):
    chat = await chat_service.create(chat_service.dto.CreateChat(agent_id=params.agent_id, organization_id=organization_id, name=params.name, system_prompt=params.system_prompt))
    return chat