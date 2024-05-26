from __future__ import annotations

from enum import StrEnum

from models.user import UserModel
from models.utils import CleverBaseModel as BaseModel


class Roles(StrEnum):
    admin: str = "Администратор"
    teacher: str = "Воспитатель"
    sitter: str = "Нянечка"
    parent: str = "Родитель"


class UserRole(StrEnum):
    PARENT = "parent"
    EMPLOYEE = "employee"
    UNKNOWN = "unknown"


class UserRoleResponse(BaseModel):
    role: UserRole = UserRole.UNKNOWN
    data: UserModel | None = None
