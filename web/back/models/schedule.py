from __future__ import annotations

from datetime import date, datetime
from uuid import uuid4

from models.utils import CleverBaseModel as BaseModel


class ScheduleModel(BaseModel):
    schedule_id: str | None = uuid4()
    presentation_id: str
    start_lesson: datetime
    end_lesson: datetime | None = None
    canceled: bool = False


class ScheduleModelResponse(BaseModel):
    schedule_id: str
    presentation_id: str | None = None
    child_ids: list[str] | None = None
    date_day: date
    is_for_child: bool = False
