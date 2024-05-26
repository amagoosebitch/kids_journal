from __future__ import annotations

from uuid import uuid4

from models.utils import CleverBaseModel as BaseModel


class PresentationModel(BaseModel):
    presentation_id: str = uuid4()
    name: str
    description: str | None = None
    photo_url: str | None = None
    file_url: str | None = None
    subject_id: str = uuid4()
