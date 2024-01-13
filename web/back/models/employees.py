from uuid import UUID, uuid4

from pydantic import BaseModel

from models.entity import Gender


class EmployeeModel(BaseModel):
    employee_id: UUID = uuid4()
    name: str
    first_name: str
    last_name: str | None = None
    email: str | None = None
    gender: Gender
    phone_number: str | None = None
    tg_user_id: str | None = None
    role_id: UUID
    group_ids: list[UUID] = []
