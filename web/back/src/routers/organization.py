from __future__ import annotations

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


async def get_organizations_for_user_by_phone(
    phone_number: str,
    organization_service=Depends(create_organization_service),
) -> list[str]:
    return organization_service.get_names_for_user(phone_number)


async def get_organization(
    organization_id: str,
    organization_service=Depends(create_organization_service),
) -> OrganizationModel | None:
    return organization_service.get_by_id(organization_id)


async def delete_organization(
    organization_id: str,
    organization_service=Depends(create_organization_service),
) -> None:
    return organization_service.delete_by_id(organization_id=organization_id)
