from uuid import UUID

from fastapi import Depends

from db.services.organization import OrganizationModel
from db.services.presentations import PresentationService
from models.presentations import PresentationModel
from src.dependencies import create_presentation_service


async def create_presentation(
    subject_id: str,
    presentation: PresentationModel,
    presentation_service: PresentationService = Depends(create_presentation_service),
) -> None:
    presentation_service.create_presentation(presentation)
    presentation_service.create_subject_presentations_pair(
        str(subject_id), str(presentation)
    )


async def get_presentation(
    organization_id: str,
    subject_id: str,
    presentation_id: str,
    presentation_service: PresentationService = Depends(create_presentation_service),
) -> PresentationModel | None:
    return presentation_service.get_by_id(str(presentation_id))


async def get_presentations(
    subject_id: str,
    presentation_service: PresentationService = Depends(create_presentation_service),
) -> PresentationModel | None:
    return presentation_service.get_all_for_subject(subject_id)
