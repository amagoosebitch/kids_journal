from fastapi import Depends, Path, Body

from db.services.skills import SkillModel, SkillLevelModel
from models.skills import ChildSkillModel
from src.dependencies import create_skill_service


async def upsert_skill(
    skill: SkillModel,
    skill_service=Depends(create_skill_service),
) -> None:
    skill_service.upsert_skill(skill)


async def get_skill_by_id(
    skill_id: str = Path(...),
    skill_service=Depends(create_skill_service),
) -> SkillModel:
    return skill_service.get_skill_by_id(skill_id)


async def get_all_skills(
    skill_service=Depends(create_skill_service),
) -> list[SkillModel]:
    return skill_service.get_all_skills()


async def upsert_skill_level(
    skill_level: SkillLevelModel,
    skill_service=Depends(create_skill_service),
) -> None:
    skill_service.upsert_skill_level(skill_level)


async def get_skill_level_by_id(
    skill_level_id: str = Path(...),
    skill_service=Depends(create_skill_service),
) -> SkillLevelModel:
    return skill_service.get_skill_level_by_id(skill_level_id)


async def get_all_skill_levels(
    skill_service=Depends(create_skill_service),
) -> list[SkillModel]:
    return skill_service.get_all_skill_levels()


async def upsert_skill_for_child(
    child_id: str,
    skill_id: str = Path(...),
    skill_level_id: str = Body(...),
    skill_service=Depends(create_skill_service)
) -> None:
    skill_service.unlink_from_child(child_id=child_id, skill_id=skill_id)
    skill_service.link_to_child(child_id=child_id, skill_id=skill_id, skill_level_id=skill_level_id)


async def get_all_skills_for_child(
    child_id: str,
    skill_service=Depends(create_skill_service)
) -> ChildSkillModel:
    return skill_service.get_all_skills_for_child(child_id=child_id)
