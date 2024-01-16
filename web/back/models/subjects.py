from uuid import UUID, uuid4

from pydantic import BaseModel


class SubjectModel(BaseModel):
    subject_id: UUID = uuid4()
    name: str
    description: str | None = None
    # photo_url: str | None = None
    age_range: str | None = None
