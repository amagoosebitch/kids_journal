from uuid import uuid4

from models.utils import CleverBaseModel as BaseModel

from models.entity import Gender
from models.role import Role


class EmployeeModel(BaseModel):
    employee_id: str = uuid4()
    name: str
    first_name: str
    last_name: str | None = None
    email: str | None = None
    gender: Gender | None = None
    phone_number: str | None = None
    tg_user_id: str | None = None
    role_id: Role | None = None
    group_ids: list[str] = []


class EmployeeResponse(BaseModel):
    employee_id: str = uuid4()
    name: str
    phone_number: str | None = None
    role_id: Role | None = None
