from uuid import uuid4

from models.utils import CleverBaseModel as BaseModel


class SubjectModel(BaseModel):
    subject_id: str = uuid4()
    name: str
    description: str | None = None
    age_range: str | None = None
