from uuid import uuid4

from models.utils import CleverBaseModel as BaseModel

from models.entity import AgeRanges


class GroupModel(BaseModel):
    group_id: str = uuid4()
    organization_id: str
    name: str
    age_range: AgeRanges


class GroupChildModel(BaseModel):
    group_id: str = uuid4()
    child_ids: list[str] = []
