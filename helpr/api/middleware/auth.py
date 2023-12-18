import json
from typing import List
from fastapi.responses import JSONResponse
from requests import HTTPError
from sqlalchemy import select
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Depends, Request, HTTPException
import jwt
from helpr import db
from helpr.api.error.base import ApiNoTokenException, ApiNotAllowedPermissionException, ApiNotValidTokenException
from helpr.db.models import user_organization
from helpr.logger import logger
from helpr.api.jwt_auth import jwt_user_auth
from helpr.organizations.permissions import Permission, PermissionRole, role_permissions
from ..request import AuthRequest, AuthedRequest


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        request = AuthRequest.from_request(request)
        logger.info(request.headers)
        if not request.access_token:
            # TODO: this works but seem kinda bad...
            return ApiNoTokenException().to_response(request)
        user_id = jwt_user_auth.decode(request.access_token)
        if not user_id:
            return ApiNotValidTokenException().to_response(request)
        request.state.user_id = user_id

        # process the request and get the response
        response = await call_next(request)

        return response



#TODO: perhaps this should also be a service that does not return api errors, and it put under organizations/permissions.py, and can be used by any service? or maybe not because a service maybe should not know how it is limited by permissions

class PermissionChecker:
    
    def __init__(self, allowed_permissions: List[Permission] = [], allowed_roles: List[PermissionRole] = []) -> None:
        self.allowed_permissions = allowed_permissions
        self.allowed_roles = allowed_roles

    async def __call__(self, user_id, organization_id: int) -> bool:
        async with db.session() as session:
            user_organization = (await session.execute(select(db.models.DBUserOrganization).where((db.models.DBUserOrganization.user_id == user_id) & (db.models.DBUserOrganization.organization_id == organization_id)))).scalar_one_or_none()
            await session.commit()
        if not user_organization:
            raise ApiNotAllowedPermissionException()
        if len(self.allowed_permissions) > 0:
            if not set(role_permissions[user_organization.role]).intersection(set(self.allowed_permissions)):
                raise ApiNotAllowedPermissionException()
        if len(self.allowed_roles) > 0:
            if user_organization.role not in self.allowed_roles:
                raise ApiNotAllowedPermissionException()
        return True
