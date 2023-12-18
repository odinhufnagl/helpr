from typing import Any, Dict, Optional
from typing_extensions import Annotated, Doc
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from helpr.logger import logger


#TODO: pretty reptitive, would maybe like it to be handled more nice
#or maybe there should be freedom, because maybe we want to do something special on a certain exception

class ApiException(Exception):
    
    def to_response(self, req: Request):
        return self.exception_handler(req, self)

    @staticmethod
    def exception_handler(request: Request, exc: 'ApiException'):
        return JSONResponse(status_code=500, content={"message": "Something went wrong"})
    
    @classmethod
    def add_to_app(cls, app):
        app.add_exception_handler(cls, cls.exception_handler)
   
   
class ApiWrongEmailPasswordException(ApiException):
    
    @staticmethod
    def exception_handler(request: Request, exc: 'ApiException'):
        return JSONResponse(status_code=402, content={"message": "Wrong email or password"})
    
    
class ApiNoTokenException(ApiException):

    @staticmethod
    def exception_handler(request: Request, exc: 'ApiException'):
        return JSONResponse(status_code=401, content={"message": "No token provided"})
    
  
class ApiNotValidTokenException(ApiException):

    @staticmethod
    def exception_handler(request: Request, exc: 'ApiException'):
        return JSONResponse(status_code=401, content={"message": "Not valid token"})
    
  
class ApiNotAllowedPermissionException(ApiException):
    
    @staticmethod
    def exception_handler(request: Request, exc: 'ApiException'):
        return JSONResponse(status_code=401, content={"message": "Not allowed permission"})