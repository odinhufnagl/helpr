from contextlib import asynccontextmanager
import os
import sys
from helpr.api.error.base import ApiException, ApiNoTokenException, ApiNotValidTokenException, ApiWrongEmailPasswordException
from helpr.api.jwt_auth import jwt_user_auth
from helpr.api.middleware.auth import AuthMiddleware, PermissionChecker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from celery import Celery, shared_task
from dotenv import load_dotenv
from sqlalchemy import select, text

from logger import logger
from fastapi import Depends, FastAPI, HTTPException
from fastapi import BackgroundTasks, FastAPI
from fastapi.security import OAuth2PasswordBearer
from .routers import about_router, auth_router, check_auth_router, organization_router, chat_session_router
from .error import all_api_exception_classes
app_with_auth = FastAPI()
load_dotenv()

#TODO: app_with_auth, app_no_auth maybe should be renamed to something like app_organization and something else for the other one  

app_with_auth.add_middleware(AuthMiddleware)
app_with_auth.include_router(about_router)
app_with_auth.include_router(check_auth_router)
app_with_auth.include_router(organization_router)


app_no_auth = FastAPI()
app_no_auth.include_router(auth_router)
#TODO: this has to be looked at, there has to be some type of auth here with a temporary cookie/session
app_no_auth.include_router(chat_session_router)


app = FastAPI()
app.mount(app=app_with_auth, path= "/app")
app.mount(app=app_no_auth, path= "")


app.add_exception_handler(Exception, ApiException.exception_handler)
app_with_auth.add_exception_handler(Exception, ApiException.exception_handler)
app_no_auth.add_exception_handler(Exception, ApiException.exception_handler)

for cls in all_api_exception_classes:
  app.add_exception_handler(cls, cls.exception_handler)
  app_with_auth.add_exception_handler(cls, cls.exception_handler)
  app_no_auth.add_exception_handler(cls, cls.exception_handler)




@app.on_event('startup')
async def on_start():
  load_dotenv()


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host='0.0.0.0', port=port, log_level="debug")
    

    