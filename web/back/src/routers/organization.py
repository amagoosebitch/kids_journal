from uuid import UUID

from fastapi import Depends

from db.services.organization import OrganizationModel
from src.dependencies import create_organization_service


async def create_organization(
    organization: OrganizationModel,
    organization_service=Depends(create_organization_service),
) -> None:
    organization_service.create_organization(organization)


async def get_organizations(
    organization_service=Depends(create_organization_service),
) -> list[OrganizationModel]:
    return organization_service.get_all()


async def get_organization(
    organization_id: UUID,
    organization_service=Depends(create_organization_service),
) -> OrganizationModel | None:
    return organization_service.get_by_id(organization_id)
