


from dataclasses import dataclass

from models.course import BaseCourse

from typing import List

from db.models.teacher import DBTeacher

@dataclass
class BaseTeacher:
    name: str
    
    @staticmethod
    def from_model(db_model: DBTeacher):
        return BaseTeacher(name=db_model.name)
