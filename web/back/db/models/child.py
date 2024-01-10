from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel

from db.entity import Gender


class ChildModel(BaseModel):
    child_id: UUID = uuid4()
    name: str
    first_name: str
    last_name: str | None = None
    birth_date: datetime | None = None
    start_education_date: datetime | None = None
    start_education_time: datetime | None = None
    end_education_time: datetime | None = None
    gender: Gender
    parent_1_id: UUID = uuid4()
    parent_2_id: UUID = uuid4()
