from datetime import datetime
from uuid import uuid4

from models.utils import CleverBaseModel as BaseModel


class ScheduleModel(BaseModel):
    schedule_id: str = uuid4()
    group_id: str
    teacher_id: str | None = None
    subject_id: str
    presentation_id: str
    start_lesson: datetime
    end_lesson: datetime | None = None
    child_id: list[str] | None = None
    description: str | None = None
    note_id: str | None = None
    canceled: bool = False


class ScheduleModelResponse(BaseModel):
    schedule_id: str
    subject_name: str | None = None
    presentation_id: str | None = None
    group_name: str | None = None
    child_names: list[str] | None = None
    date_day: datetime
    description: str | None = None
    is_for_child: bool = False
