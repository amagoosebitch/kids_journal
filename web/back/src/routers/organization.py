from uuid import UUID

from fastapi import Depends
from starlette.responses import Response

from db.services.organization import OrganizationModel
from src.dependencies import create_organization_service


async def create_organization(
    organization: OrganizationModel,
    organization_service=Depends(create_organization_service),
):
    response = organization_service.create_organization(organization)

    return {
        "organization_id": response.organization_id
    }


async def get_organizations(
    organization_service=Depends(create_organization_service),
):
    response = organization_service.get_all()

    return response


async def get_organization(
    organization_id: UUID,
    organization_service=Depends(create_organization_service),
):
    response = organization_service.get_by_id(organization_id)

    if not response:
        return Response("Organization not found", status_code=404)

    return Response(response.json(), status_code=200)
