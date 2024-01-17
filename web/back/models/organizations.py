from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel


class OrganizationModel(BaseModel):
    organization_id: str = uuid4()
    name: str
    description: str | None = None
    photo_url: str | None = None
    start_education_time: datetime = datetime.utcnow()
    end_education_time: datetime = datetime.utcnow()
    registration_date: datetime = datetime.utcnow()
    updated_date: datetime = datetime.utcnow()
