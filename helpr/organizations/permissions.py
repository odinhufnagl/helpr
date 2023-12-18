
from enum import Enum
from typing import List, Literal

PermissionRole = Literal['admin']
#TODO: just dummy so far
Permission = Literal['chat.read', 'training.write']

role_permissions: dict[PermissionRole, List[Permission]] = {'admin': ['chat.read', 'training.write']}

