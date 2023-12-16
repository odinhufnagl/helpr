import json
from fastapi.responses import JSONResponse
from requests import HTTPError
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Depends, Request, HTTPException
import jwt
from plannr.api.error.base import ApiNoTokenException, ApiNotValidTokenException

from plannr.logger import logger
from plannr.api.jwt_auth import jwt_user_auth
from ..request import AuthRequest, AuthedRequest

class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        request = AuthRequest.from_request(request)
        logger.info(request.headers)
        if not request.access_token:
            #TODO: this works but seem kinda bad...
            return ApiNoTokenException().to_response(request)
        user_id = jwt_user_auth.decode(request.access_token)
        if not user_id:
            return ApiNotValidTokenException().to_response(request)

        request.state.user_id = user_id

        # process the request and get the response    
        response = await call_next(request)
        
        return response