from uuid import uuid4
from models.utils import CleverBaseModel as BaseModel

from models.entity import Gender


class ParentModel(BaseModel):
    parent_id: str = uuid4()
    name: str
    first_name: str
    last_name: str | None = None
    email: str | None = None
    gender: Gender | None = None
    phone_number: str | None = None
    freq_notifications: int = 0
    tg_user_id: str | None = None


class ParentModelResponse(BaseModel):
    parent_id: str
    name: str
    phone_number: str | None = None
