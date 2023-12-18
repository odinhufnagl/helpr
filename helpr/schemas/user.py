from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from helpr.schemas.base import BaseSchema
from helpr.schemas.organization import OrganizationSchema

@dataclass
class UserSchema(BaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    email: str
    organizations: Optional[List[OrganizationSchema]] = None
    