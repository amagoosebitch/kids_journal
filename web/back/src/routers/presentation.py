from uuid import UUID

from fastapi import Depends

from db.services.organization import OrganizationModel
from db.services.presentations import PresentationService
from models.presentations import PresentationModel
from src.dependencies import create_presentation_service


async def create_presentation(
    subject_id: UUID,
    presentation: PresentationModel,
    presentation_service: PresentationService = Depends(create_presentation_service),
) -> None:
    presentation_service.create_presentation(presentation)
    presentation_service.create_subject_presentations_pair(
        str(subject_id), str(presentation)
    )


async def get_presentation(
    organization_id: UUID,
    subject_id: UUID,
    presentation_id: UUID,
    presentation_service: PresentationService = Depends(create_presentation_service),
) -> OrganizationModel | None:
    return presentation_service.get_by_id(str(presentation_id))
