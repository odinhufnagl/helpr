from dataclasses import dataclass
from typing import List, Optional
from models.school import BaseSchool
from db.models.class_group import DBClassGroup

@dataclass
class ClassGroup:
    name: str
    code: str
    school_id: int
    school: Optional[BaseSchool]
    
    @staticmethod
    def from_model(db_model: DBClassGroup):
        return ClassGroup(db_model.name, db_model.code, db_model.school_id, db_model.school)
        
