from __future__ import annotations

from fastapi import Depends, Path

import src.routers.skills as skills
from db.services.presentations import PresentationService
from db.services.skills import SkillService
from models.presentations import PresentationModel
from models.skills import SkillModel
from src.dependencies import create_presentation_service, create_skill_service


async def upsert_presentation(
    presentation: PresentationModel,
    subject_id: str = Path(...),
    presentation_service: PresentationService = Depends(create_presentation_service),
) -> None:
    presentation_service.upsert_presentation(presentation)


async def get_presentation(
    presentation_id: str,
    presentation_service: PresentationService = Depends(create_presentation_service),
) -> PresentationModel | None:
    return presentation_service.get_by_id(str(presentation_id))


async def get_all_presentations_for_subject(
    subject_id: str,
    presentation_service: PresentationService = Depends(create_presentation_service),
) -> list[PresentationModel] | None:
    return presentation_service.get_all_for_subject(subject_id)


async def delete_presentation(
    presentation_id: str, presentation_service=Depends(create_presentation_service)
) -> None:
    return presentation_service.delete_by_id(presentation_id=presentation_id)
