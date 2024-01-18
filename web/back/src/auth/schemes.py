from models.utils import CleverBaseModel as BaseModel


class TelegramAuth(BaseModel):
    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    photo_url: str | None = None
    auth_date: str | None = None
    hash: str | None = None
