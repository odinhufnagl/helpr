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
from helpr.api.request.base import ClientAuthRequest
from helpr.db.models import user_organization
from helpr.logger import logger
from helpr.api.jwt_auth import jwt_user_auth, jwt_client_auth
from helpr.organizations.permissions import Permission, PermissionRole, role_permissions
from ..request import AuthRequest, AuthedRequest


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        request = ClientAuthRequest.from_request(request)
        logger.info(request.headers)
        if not request.access_token:
            # TODO: this works but seem kinda bad...
            return ApiNoTokenException().to_response(request)
        chat_session_id = jwt_client_auth.decode(request.access_token)
        if not chat_session_id:
            return ApiNotValidTokenException().to_response(request)
        request.state.chat_session_id = chat_session_id

        # process the request and get the response
        response = await call_next(request)

        return response

