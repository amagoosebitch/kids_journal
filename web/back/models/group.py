from __future__ import annotations

from uuid import uuid4

from models.entity import AgeRanges
from models.utils import CleverBaseModel as BaseModel


class GroupModel(BaseModel):
    group_id: str | None = uuid4()
    organization_id: str
    name: str
    age_range: AgeRanges
