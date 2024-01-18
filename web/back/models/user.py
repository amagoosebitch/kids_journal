from enum import StrEnum

from models.utils import CleverBaseModel as BaseModel

from models.employees import EmployeeModel
from models.parents import ParentModel


class UserRole(StrEnum):
    PARENT = "parent"
    EMPLOYEE = "employee"
    UNKNOWN = "unknown"


class UserModelResponse(BaseModel):
    role: UserRole = UserRole.UNKNOWN
    data: ParentModel | EmployeeModel | None = None


class MergeUserModel(BaseModel):
    phone_number: str
    tg_user_id: str
