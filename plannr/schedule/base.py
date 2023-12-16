from dataclasses import dataclass
from enum import Enum
from optparse import Option

from sre_parse import State
from typing import List, Optional
from prettytable import PrettyTable
from sqlalchemy import select, update
from models import BaseTeacher, ClassGroup, BaseEvent, ClassGroupsEvent, ClassRoomsEvent, Lecture, TeachersEvent, ClassRoom
import db
from db.models.event import DBEvent
from db.models.schedule import DBSchedule


# TODO: add the correct values to the store_to_db

@dataclass
class BaseSchedule:
    class State(Enum):
        ONGOING = "ongoing"
        CREATING = "creating"
        FINISHED = "finished"

    schedule_id: Optional[int]
    coalition_id: Optional[int]
    state: State
    events: List[BaseEvent]

    def add_event(self, event: BaseEvent):
        self.events.append(event)

    @staticmethod
    def from_model_events(db_events: List[DBEvent]) -> 'BaseSchedule':
        events = list(map(lambda e: BaseEvent.from_model(e), db_events))
        return BaseSchedule(None, events)

    async def store_to_db(self):
        async with db.session() as session:
            if self.schedule_id:
                db_schedule = (await session.execute(select(db.models.DBSchedule).where(db.models.DBSchedule.id == self.schedule_id))).scalar()
                db_schedule.state = self.state.name
                db_schedule.coalition_id = self.coalition_id
            else:
                db_schedule = db.models.DBSchedule(
                    coalition_id=self.coalition_id, state=self.state.name)
                session.add(db_schedule)
            await session.commit()
        self.schedule_id = db_schedule.id

        async with db.session() as session:
            db_events: List[DBEvent] = list(map(lambda e: e.to_model(
                schedule_id=self.schedule_id, ongoing=False), self.events))
            session.add_all(db_events)
            await session.commit()

    def print(self):
        pass


class OngoingSchedule:
    schedule_id: Optional[int]
    events: List[BaseEvent]

    async def store_to_db(self):
        async with db.session() as session:
            if not self.schedule_id:
                db_schedule = db.models.DBSchedule()
                session.add(db_schedule)
                await session.commit()
                self.schedule_id = db_schedule.id
        async with db.session() as session:
            db_events: List[DBEvent] = list(map(lambda e: e.to_model(
                schedule_id=self.schedule_id, ongoing=True), self.events))
            session.add(db_events)
            await session.commit()


@dataclass
class ClassGroupSchedule(BaseSchedule):
    events: List[ClassGroupsEvent]
    class_group: Optional[ClassGroup]
    class_group_id: int

    def print(self):
        table = PrettyTable()
        table.field_names = ["Day", "Time Interval", "Event Type", "Teacher"]

        for event in self.events:
            time_interval = f"{event.interval.start_time}-{event.interval.end_time}"
            event_type = type(event).__name__
            details = ""

            if isinstance(event, Lecture):
                details = f"{event.course_id}/{event.course_id}"
            table.add_row([time_interval, event_type, details])

        print(table)


@dataclass
class TeacherSchedule(BaseSchedule):
    events: List[TeachersEvent]
    teacher: Optional[BaseTeacher]
    teacher_id: int

    def print(self):
        table = PrettyTable()
        table.field_names = ["Day", "Time Interval",
                             "Event Type", "ClassGroup"]

        for event in self.events:

            time_interval = f"{event.interval.start_time}-{event.interval.end_time}"
            event_type = type(event).__name__
            details = ""

            if isinstance(event, Lecture):
                details = f"{event.course_id}"
            table.add_row([time_interval, event_type, details])

        print(table)


@dataclass
class ClassRoomSchedule(BaseSchedule):
    events: List[ClassRoomsEvent]
    class_room: Optional[ClassRoom]
    class_room_id: int
