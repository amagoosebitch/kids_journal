from uuid import UUID, uuid4

from pydantic import BaseModel


class PresentationModel(BaseModel):
    presentation_id: str = uuid4()
    name: str
    description: str | None = None
    photo_url: str | None = None
    file_url: str | None = None
