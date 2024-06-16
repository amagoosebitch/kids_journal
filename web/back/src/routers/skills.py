from fastapi import Body, Depends, Path

from db.services.skills import SkillLevelModel, SkillModel
from models.skills import ChildSkillModel
from src.dependencies import create_skill_service


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
) -> list[SkillLevelModel]:
    return skill_service.get_all_skill_levels()


async def upsert_skill_for_child(
    skill_level_id: str,
    child_id: str,
    presentation_id: str = Path(...),
    skill_service=Depends(create_skill_service),
) -> None:
    skill_service.unlink_from_child(child_id=child_id, presentation_id=presentation_id)
    skill_service.link_to_child(
        child_id=child_id,
        presentation_id=presentation_id,
        skill_level_id=skill_level_id,
    )


async def get_all_skills_for_child(
    child_id: str, skill_service=Depends(create_skill_service)
) -> list[ChildSkillModel]:
    return skill_service.get_all_skills_for_child(child_id=child_id)


async def delete_skill_level(
    skill_level_id: str, skill_service=Depends(create_skill_service)
) -> None:
    return skill_service.delete_by_id(skill_level_id=skill_level_id)
