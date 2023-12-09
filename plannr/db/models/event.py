from datetime import datetime
from enum import Enum
from typing import List, Optional
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from .util import Base, id_column, created_at_column, updated_at_column

class DBEvent(Base):
    class Type(Enum):
        TEACHER_LUNCH = "teacher_lunch_event"
        CLASSGROUP_LUNCH = "classgroup_lunch_event"
        LECTURE = "lecture_event"
        
    __tablename__ = "event"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    ongoing: Mapped[bool] = mapped_column(Boolean, default=True)
    schedule_id: Mapped[int] = mapped_column(ForeignKey('schedule.id'), nullable=True)
    type: Mapped[Type]
    __mapper_args__ = {
        "polymorphic_identity": "event",
        "polymorphic_on": "type",
    }
    
    
class DBTeacherEventBrigde(Base):
    __tablename__ = "teacher_event_bridge"
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"), primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), primary_key=True)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    
    
    
class DBClassRoomEventBridge(Base):
    __tablename__ = "class_room_event_bridge"
    teacher_id: Mapped[int] = mapped_column(ForeignKey("class_room.id"), primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), primary_key=True)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    
    
class DBClassGroupEventBridge(Base):
    __tablename__ = "class_group_event_bridge"
    teacher_id: Mapped[int] = mapped_column(ForeignKey("class_group.id"), primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), primary_key=True)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    
    
#TODO: should be multiple teachers, classgroups etc
class DBTeacherLunchEvent(DBEvent):
    __tablename__ = "teacher_lunch_event"
    id: Mapped[int] = mapped_column(ForeignKey("event.id"), primary_key=True)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    teachers: Mapped[List['DBTeacher']] = relationship('DBTeacher', secondary='teacher_event_bridge') #type: ignore
    
    __mapper_args__ = {
        "polymorphic_identity": "teacher_lunch",
    }
    
class DBClassGroupLunchEvent(DBEvent):
    __tablename__ = "classgroup_lunch_event"
    id: Mapped[int] = mapped_column(ForeignKey("event.id"), primary_key=True)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    class_groups: Mapped[List['DBClassGroup']] = relationship('DBClassGroup', secondary='class_group_event_bridge') #type: ignore
    
    __mapper_args__ = {
        "polymorphic_identity": "classgroup_lunch",
    }
    
    
    
class DBLectureEvent(DBEvent):
    __tablename__ = "lecture_event"
    id: Mapped[int] = mapped_column(ForeignKey("event.id"), primary_key=True)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))
    course: Mapped['DBCourse'] = relationship() #type: ignore
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"))
    school: Mapped['DBSchool'] = relationship() #type: ignore
    teachers: Mapped[List['DBTeacher']] = relationship('DBTeacher', secondary='teacher_event_bridge') #type: ignore
    class_rooms: Mapped[List['DBClassRoom']] = relationship('DBClassRoom', secondary='class_room_event_bridge') #type: ignore
    class_groups: Mapped[List['DBClassGroup']] = relationship('DBClassGroup', secondary='class_group_event_bridge') #type: ignore
    
    __mapper_args__ = {
        "polymorphic_identity": "lecture",
    }
    
    
