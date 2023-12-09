
from dataclasses import dataclass
from typing import List, Optional
from models.school.base import BaseSchool
from db.models.coalition import DBCoalition


@dataclass
class BaseCoalition:
    name: str
    schools: Optional[List[BaseSchool]]
    
    @staticmethod
    def from_model(db_model: DBCoalition):
        return BaseCoalition(db_model.name, db_model.schools)