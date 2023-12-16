from contextlib import asynccontextmanager
import os
import sys
from plannr.api.jwt_auth import jwt_user_auth
from plannr.api.middleware.auth import AuthMiddleware
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from celery import Celery, shared_task
from dotenv import load_dotenv
from sqlalchemy import select, text

from logger import logger
from fastapi import Depends, FastAPI
from fastapi import BackgroundTasks, FastAPI
from .routers import about_router, admin_router, schedule_router, auth_router, check_auth_router

app_with_auth = FastAPI()
load_dotenv()



app_with_auth.add_middleware(AuthMiddleware)
app_with_auth.include_router(about_router)
app_with_auth.include_router(admin_router)
app_with_auth.include_router(schedule_router)
app_with_auth.include_router(check_auth_router)

app_no_auth = FastAPI()
app_no_auth.include_router(auth_router)


app = FastAPI()
app.mount(app=app_with_auth, path= "/app")
app.mount(app=app_no_auth, path= "")


@app.on_event('startup')
async def on_start():
  load_dotenv()


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host='0.0.0.0', port=port, log_level="debug")
    

    