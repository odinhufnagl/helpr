import logging
from math import log
from taskqueue import Queue
from celery import Celery, shared_task
from dotenv import load_dotenv
from sqlalchemy import select
import db
from flask import Flask, render_template, request
from fastapi import FastAPI, Request
import sys
import asyncio
import os
from controllers.schedule import CoalitionScheduleController
from pydantic import BaseModel
from fastapi import BackgroundTasks, FastAPI
from logger import logger
from schedule.base import BaseSchedule
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = FastAPI()
load_dotenv()
queue = Queue()

# TODO: these are just dummy routes


class PostAdminRequest(BaseModel):
    email: str
    password: str

@app.post('/admin')
async def post_admin(request: PostAdminRequest):
    print("req", request.json)
    async with db.session() as session:
        db_user = db.models.DBUser(
            email=request.email, password=request.password)
        session.add(db_user)
        await session.flush()
        db_admin = db.models.DBAdmin(user_id=db_user.id)
        session.add(db_admin)
        await session.commit()
    return "Success"


# About page
@app.get('/about')
def about():
    return 'Plannr is a system that helps teacher to create schedules'



class CreateSheduleRequest(BaseModel):
    admin_id: int
    coalition_id: int

@app.post("/create_schedule")
async def create_schedule(request: CreateSheduleRequest):
    schedule_controller = CoalitionScheduleController(coalition_id=request.coalition_id)
    new_schedule_id = await schedule_controller.create_new_schedule()
    return new_schedule_id
   


    
@app.get("/schedule/{schedule_id}")
async def get_schedule(schedule_id: int):
    async with db.session() as session:
        schedule = (await session.execute(select(db.models.DBSchedule).where(db.models.DBSchedule.id == schedule_id))).scalar_one_or_none()
    return schedule


@app.on_event('startup')
async def on_start():
  load_dotenv()
  await db.init()
  



if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host='0.0.0.0', port=port, debug=True, log_level="debug")
    

    