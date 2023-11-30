


from dataclasses import dataclass

from plannr.models.course.base import BaseCourse
from typing import List

@dataclass
class BaseTeacher:
    name: str
