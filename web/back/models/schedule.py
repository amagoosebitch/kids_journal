from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel


class ScheduleModel(BaseModel):
    schedule_id: UUID = uuid4()
    group_id: UUID
    teacher_id: UUID
    subject_id: UUID
    presentation_id: UUID
    start_lesson: datetime
    end_lesson: datetime
    child_id: list[UUID] | None = None
    description: str | None = None


class ScheduleModelResponse(BaseModel):
    schedule_id: UUID
    subject_name: str | None = None
    group_name: str | None = None
    child_names: list[str] | None = None
    date: datetime
    description: str | None = None
    is_for_child: bool = False
