from __future__ import annotations

from uuid import uuid4

from models.utils import CleverBaseModel as BaseModel

from models.entity import Gender


class UserModel(BaseModel):
    employee_id: str = uuid4()
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: str | None = None
    gender: Gender | None = None
    phone_number: str | None = None
    tg_user_id: str | None = None


class UserModelResponse(BaseModel):
    user_id: str = uuid4()
    name: str
    phone_number: str | None = None


class MergeUserModel(BaseModel):
    phone_number: str
    tg_user_id: str




