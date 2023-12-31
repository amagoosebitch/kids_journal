from uuid import UUID, uuid4

from pydantic import BaseModel

from db.entity import Gender


class ParentModel(BaseModel):
    parent_id: UUID = uuid4()
    name: str
    first_name: str
    last_name: str | None = None
    email: str | None = None
    gender: Gender
    phone_number: str | None = None
    freq_notifications: int
    tg_user_id: str | None = None
