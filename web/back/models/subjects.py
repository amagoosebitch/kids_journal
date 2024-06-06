from __future__ import annotations

from uuid import uuid4

from models.utils import CleverBaseModel as BaseModel


class SubjectModel(BaseModel):
    subject_id: str | None = uuid4()
    name: str
    description: str | None = None
    age_range: str | None = None
