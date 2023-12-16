from uuid import UUID

from fastapi import Depends
from starlette.responses import Response

from db.services.organization import OrganizationModel
from src.dependencies import create_organization_service
from src.routers.routers import router


@router.post("/organizations", status_code=201)
async def create_organization(
    organization: OrganizationModel,
    organization_service=Depends(create_organization_service),
):
    response = organization_service.create_organization(organization)

    return {
        "organization_id": response.organization_id
    }  # посмотреть че возвращает запрос


@router.get("/organizations")
async def get_organizations(
    organization_service=Depends(create_organization_service),
):
    response = organization_service.get_all()

    return response  # посмотреть че возвращает запрос


@router.get("/organizations/{organization_id}")
async def get_organization(
    organization_id: UUID,
    organization_service=Depends(create_organization_service),
):
    response = organization_service.get_by_id(organization_id)

    if not response:
        return Response("Organization not found", status_code=404)

    return Response(response.json(), status_code=200)
