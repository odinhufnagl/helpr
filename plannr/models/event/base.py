

from dataclasses import dataclass
from typing import List, Optional
from models.classgroup.base import ClassGroup
from models.classroom.base import ClassRoom
from models.course.base import BaseCourse
from models.school.base import BaseSchool
from models.teacher.base import BaseTeacher
from common.date import TimeInterval
from db.models.event import DBEvent, DBLectureEvent
from enum import Enum, auto
import db


@dataclass
class BaseEvent:
    id: Optional[int]
    interval: TimeInterval

    @staticmethod
    def from_model(db_event: DBEvent) -> 'BaseEvent':
        time_interval = TimeInterval(db_event.start_time, db_event.end_time)
        db_event_to_event = {DBEvent.Type.TEACHER_LUNCH: TeachersLunch(db_event.id, time_interval, None), 
                         DBEvent.Type.CLASSGROUP_LUNCH: ClassGroupsLunch(db_event.id, time_interval, None),
                         DBEvent.Type.LECTURE: Lecture.from_model(db_event)
                         }
        return db_event_to_event[db_event.type]
    
    #TODO: on all store_to_db, fill them out with the params
    def to_model(self, schedule_id: Optional[int], ongoing: bool):
        return db.models.DBEvent(schedule_id=schedule_id, ongoing=ongoing)
        
    
    #TODO: on all store_to_db, fill them out with the params
    async def store_to_db(self):
         async with db.session() as session:
            if not self.id:
                db_event = db.models.DBEvent()
                session.add(db_event)
                await session.commit()

       

        


#TODO: have to decide if events should include multiple ex teachers. If they will, we have to edit the db so we have a bridge between teacher and event. And perhaps also have a model for it
#because it might be used a lot
#EDIT: a lecture obviously should have multiple teachers so it make sense to have multiple teachers to each of these events

@dataclass
class TeachersEvent(BaseEvent):
    teachers: Optional[List[BaseTeacher]]


@dataclass
class ClassGroupsEvent(BaseEvent):
    class_groups: Optional[List[ClassGroup]]


@dataclass
class ClassRoomsEvent(BaseEvent):
    class_rooms: Optional[List[ClassRoom]]


@dataclass
class Lecture(TeachersEvent, ClassGroupsEvent, ClassRoomsEvent):
    course: Optional[BaseCourse]
    course_id: int
    school: Optional[BaseSchool]
    school_id: int
    
    @staticmethod
    def from_model(db_lecture: DBLectureEvent) -> 'Lecture':
        #TODO: add the teachers, class_groups, class_rooms
        teachers: List[BaseTeacher] = list(map(lambda t: BaseTeacher.from_model(t), db_lecture.teachers))
        class_groups: List[ClassGroup] = list(map(lambda cg: ClassGroup.from_model(cg), db_lecture.class_groups))
        class_rooms: List[ClassRoom] = list(map(lambda cr: ClassRoom.from_model(cr), db_lecture.class_rooms))
        return Lecture(db_lecture.id, TimeInterval(db_lecture.start_time, db_lecture.end_time), class_rooms, class_groups, teachers, db_lecture.course, db_lecture.course_id, db_lecture.school, db_lecture.school_id)
    
    def to_model(self):
        return db.models.DBEvent()
    
    async def store_to_db(self):
         async with db.session() as session:
            if not self.id:
                db_event = db.models.DBLectureEvent()
                session.add(db_event)
                await session.commit()
       
        

@dataclass
class TeachersLunch(TeachersEvent):
    def to_model(self):
        return db.models.DBEvent()
    
    async def store_to_db(self):
         async with db.session() as session:
            if not self.id:
                db_event = db.models.DBTeacherLunchEvent
                session.add(db_event)
                await session.commit()
       


@dataclass
class ClassGroupsLunch(ClassGroupsEvent):
    def to_model(self):
        return db.models.DBEvent()
    
    async def store_to_db(self):
         async with db.session() as session:
            if not self.id:
                db_event = db.models.DBClassGroupLunchEvent
                session.add(db_event)
                await session.commit()
       
