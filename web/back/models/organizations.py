from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from models.utils import CleverBaseModel as BaseModel


class OrganizationModel(BaseModel):
    organization_id: str = uuid4()
    name: str
    description: str | None = None
    photo_url: str | None = None
    start_education_time: datetime = datetime.utcnow()
    end_education_time: datetime = datetime.utcnow()
    registration_date: datetime = datetime.utcnow()
    updated_date: datetime = datetime.utcnow()
