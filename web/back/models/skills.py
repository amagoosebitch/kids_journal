from __future__ import annotations

import uuid

from models.utils import CleverBaseModel as BaseModel


class SkillModel(BaseModel):
    skill_id: str = uuid.uuid4()
    name: str
    subject_id: str
    description: str | None = None


class SkillLevelModel(BaseModel):
    skill_level_id: str = uuid.uuid4()
    name: str
    description: str | None = None


class ChildSkillModel(BaseModel):
    child_id: str
    skill_id: str
    skill_level_id: str
