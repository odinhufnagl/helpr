from dataclasses import dataclass
from scheduling.school.base import BaseSchool


@dataclass
class ClassRoom:
    name: str
    code: str
    school: BaseSchool
