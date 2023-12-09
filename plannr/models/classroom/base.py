from dataclasses import dataclass
from typing import Optional
from models.school import BaseSchool
from db.models.class_room import DBClassRoom

@dataclass
class ClassRoom:
    name: str
    code: str
    school_id: int
    school: Optional[BaseSchool]
    
    @staticmethod
    def from_model(db_model: DBClassRoom):
        return ClassRoom(db_model.name, db_model.code, db_model.school_id, db_model.school)
