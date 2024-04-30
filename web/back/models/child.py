from __future__ import annotations

from datetime import datetime

from models.utils import CleverBaseModel as BaseModel

from models.entity import Gender
from models.user import UserModelResponse


class ChildModel(BaseModel):
    child_id: str
    first_name: str
    middle_name: str | None = None
    last_name: str | None = None
    birth_date: datetime | None = None
    start_education_date: datetime | None = None
    end_education_date: datetime | None = None
    gender: Gender | None = None
    avatar_url: str |  None = None


class ChildModelResponse(BaseModel):
    child_id: str
    name: str
    birth_date: datetime | None = None
    # parent_1: UserModelResponse | None = None
    # parent_2: UserModelResponse | None = None
