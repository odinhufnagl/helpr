import json
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Depends, Request
import jwt
from helpr.logger import logger
from helpr.api.jwt_auth import JWTUserAuth

class BaseRequest(Request):
    @classmethod
    def from_request(cls, req: Request):
        return cls(req.scope, req.receive)
    
    
class AuthRequest(BaseRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_token = self.headers.get("x-access-token", None)
  
class ClientAuthRequest(BaseRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_token = self.headers.get("client-access-token", None)

class AuthedRequest(BaseRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = self.state.user_id

    
    