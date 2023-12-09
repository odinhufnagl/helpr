
from time import sleep
from typing import List
from pydantic import BaseModel
from feedback.base import BaseFeedback
from db.models.requirement import DBRequirement
from schedulers.base import DumbScheduler
from requirement.base import BaseRequirement
from schedule.base import BaseSchedule
import db
from sqlalchemy import select

class BaseScheduleGenerator(BaseModel):
    @staticmethod
    async def generate_schedule(schedule_id: int, feedback: List[BaseFeedback]) -> BaseSchedule:
        raise NotImplementedError()
    
    
#TODO: maybe rethink this? The name indicates that it should generate schedules for a certain coalition but that is not really the case
#which makes sense because for generating schedules there should already be a schedule, and then we would not need to pass the coalition-id, because it should be connected to a coalition
#maybe if we rethink and say that a schedule does not need to belong to a coalition we would need to change this so that is takes in a coalition_id, and then connects that schedule to the coalition_id
#but maybe doesnt really make sense

class CoalitionScheduleGenerator(BaseScheduleGenerator):
    
    @staticmethod
    async def generate_schedule(schedule_id: int, feedback: List[BaseFeedback]) -> BaseSchedule:
        async with db.session() as session:
            coalition_id = (await session.execute(select(db.models.DBSchedule).where(db.models.DBSchedule.id == schedule_id))).scalar_one_or_none().coalition_id
            if not coalition_id:
                #TODO: better error handling all over the app
                raise Exception()
        async with db.session() as session:
            db_reqs: List[DBRequirement] = list((await session.execute(
                select(db.models.DBRequirement)
                .where(db.models.DBRequirement.coalition_id == coalition_id)
            )).scalars().all())
            
        requirements = list(
            map(lambda r: BaseRequirement.from_model(r), db_reqs))

        new_schedule = await DumbScheduler.generate_schedule(requirements=requirements, feedback=feedback, prev_schedule=None)
        new_schedule.coalition_id = coalition_id
        new_schedule.state = BaseSchedule.State.ONGOING
        new_schedule.schedule_id = schedule_id
        await new_schedule.store_to_db()
        return new_schedule.schedule_id
    