from typing import Any
from helpr.schemas.base import BaseSchema


class VariableSchema(BaseSchema):
    id: int
    key: str
    value: Any
    organization_id: int