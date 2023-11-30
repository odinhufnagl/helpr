from dataclasses import dataclass
from src.models.school.base import BaseSchool

@dataclass
class BaseCourse:
    name: str
    code: str
    school: BaseSchool