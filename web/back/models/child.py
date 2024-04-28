from __future__ import annotations

from datetime import datetime

from models.utils import CleverBaseModel as BaseModel

from models.entity import Gender
from models.parents import ParentModelResponse


class ChildModel(BaseModel):
    child_id: str
    # name: str
    first_name: str
    middle_name: str | None = None
    last_name: str | None = None
    birth_date: datetime | None = None
    start_education_date: datetime | None = None
    # start_education_time: datetime | None = None
    end_education_date: datetime | None = None
    gender: Gender | None = None
    avatar_url: str |  None = None
    # parent_1_id: str | None = None
    # parent_2_id: str | None = None


class ChildModelResponse(BaseModel):
    child_id: str
    name: str
    birth_date: datetime | None = None
    # parent_1: ParentModelResponse | None = None
    # parent_2: ParentModelResponse | None = None
