from dataclasses import dataclass
from enum import Enum
import json
import re
from tkinter import Scale
from typing import Any, List, Optional
from unittest.mock import Base
from uu import Error

from sqlalchemy import select
from models import BaseTeacher, ClassGroup, BaseEvent, BaseSchool, ClassRoom
from db.models.event import DBEvent
from db.models.requirement import DBRequirement
from db.engine import session
from schedule import BaseSchedule
import db

# TODO: better structure so it is easy to create new requirements


@dataclass
class RequirementDeviation:
    value: int


@dataclass
class PriorityScale:
    min: int
    max: int

    def is_in_range(self, value):
        return min <= value or value <= max


@dataclass
class BaseRequirement:
    PRIORITY_MAX = 100
    PRIORITY_MIN = 0
    priority_scale = PriorityScale(PRIORITY_MIN, PRIORITY_MAX)
    priority: int

    def __init__(self, prio) -> None:
        self.set_priority(prio)

    def set_priority(self, prio: int):
        if self.priority_scale.is_in_range(prio):
            self.priority = prio
            return
        raise Error

    def deviation(self, schedule: BaseSchedule) -> RequirementDeviation:
        raise NotImplementedError

    @staticmethod
    def from_model(db_req: DBRequirement) -> 'BaseRequirement':
        db_req_to_req = {db_req.Type.TEACHER_EVENT: TeacherEventRequirement.from_model(db_req),
                         db_req.Type.CLASS_GROUP_EVENT: ClassGroupEventRequirement.from_model(
                             db_req)
                         }
        return db_req_to_req[db_req.type]


@dataclass
class EventRequirement(BaseRequirement):
    event: Optional[BaseEvent]
    event_id: int

    async def get_event(self):
        async with db.session() as session:
            db_event = (await session.execute(select(db.models.DBRequirement).where(db.models.DBRequirement.id == self.event_id))).scalar_one_or_none()
            self.event = BaseEvent.from_model(db_event)
        return self.event


@dataclass
class TeacherRequirement(BaseRequirement):
    teacher: Optional[BaseTeacher]
    teacher_id: int


@dataclass
class ClassGroupRequirement(BaseRequirement):
    class_group: Optional[ClassGroup]
    class_group_id: int


@dataclass
class ClassRoomRequirement(BaseRequirement):
    class_room: Optional[ClassRoom]
    class_room_id: int


@dataclass
class TeacherEventRequirement(TeacherRequirement, EventRequirement):

    @staticmethod
    # TODO: parse db_event and pass to eventparam
    def from_model(db_req: DBRequirement, db_event: Optional[DBEvent] = None) -> 'TeacherEventRequirement':
        params = json.loads(db_req.params)

        return TeacherEventRequirement(priority=db_req.priority, teacher=params.teacher, teacher_id=params.teacher_id, event=None, event_id=params.event_id)


@dataclass
class ClassGroupEventRequirement(ClassGroupRequirement, EventRequirement):

    @staticmethod
    # TODO: parse db_event and pass to eventparam
    def from_model(db_req: DBRequirement, db_event: Optional[DBEvent] = None) -> 'ClassGroupEventRequirement':
        params = json.loads(db_req.params)
        return ClassGroupEventRequirement(priority=db_req.priority, class_group=params.class_group, class_group_id=params.class_group_id, event=None, event_id=params.event_id)


class SchoolRequirement(BaseRequirement):
    school: BaseSchool
