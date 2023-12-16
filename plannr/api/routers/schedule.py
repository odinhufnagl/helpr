
from fastapi import APIRouter, Request
from pydantic import BaseModel
from sqlalchemy import select
from plannr.controllers.schedule import CoalitionScheduleController
import plannr.db as db
from ..request import AuthedRequest
from plannr.logger import logger

router = APIRouter(prefix='/schedule')

class GenerateShedule(BaseModel):
    coalition_id: int
    
@router.post("/generate")
async def generate_schedule(params: GenerateShedule, request: Request):
    request = AuthedRequest.from_request(request)
    logger.info(f"user_id: {request.user_id}")
    schedule_controller = CoalitionScheduleController(coalition_id=params.coalition_id)
    new_schedule_id = await schedule_controller.create_new_schedule()
    return new_schedule_id
   
@router.get("/{id}")
async def get_schedule(id: int):
    async with db.session() as session:
        schedule = (await session.execute(select(db.models.DBSchedule).where(db.models.DBSchedule.id == id))).scalar_one_or_none()
    return schedule

