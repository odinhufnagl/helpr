from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional
from pydantic import BaseModel
from helpr.organizations.permissions import PermissionRole
from helpr.schemas.base import BaseSchema

class UserOrganizationSchema(BaseSchema):
    created_at: datetime
    updated_at: datetime
    user_id: int
    organization_id: int
    role: PermissionRole
   
