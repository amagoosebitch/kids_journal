from __future__ import annotations

import uuid
from enum import StrEnum

from models.user import UserModel
from models.utils import CleverBaseModel as BaseModel


class Roles(StrEnum):
    PARENT = "parent"
    EMPLOYEE = "employee"
    UNKNOWN = "unknown"


class UserRoleResponse(BaseModel):
    role: Roles = Roles.UNKNOWN
    data: UserModel | None = None
