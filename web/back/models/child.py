from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from models.entity import Gender
from models.user import UserModelResponse
from models.utils import CleverBaseModel as BaseModel


class ChildModel(BaseModel):
    child_id: str = uuid4()
    first_name: str
    middle_name: str | None = None
    last_name: str | None = None
    birth_date: datetime | None = None
    start_education_date: datetime | None = None
    end_education_date: datetime | None = None
    gender: Gender | None = None
    avatar_url: str | None = None


class ChildModelResponse(BaseModel):
    child_id: str
    name: str
    birth_date: datetime | None = None
    # parent_1: UserModelResponse | None = None
    # parent_2: UserModelResponse | None = None
