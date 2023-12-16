from uuid import UUID

from fastapi import Depends
from starlette.responses import Response

from db.services.groups import GroupModel
from src.dependencies import create_group_service
from src.routers.routers import router


@router.post("/groups", status_code=201)
async def add_group_to_organization(
    group: GroupModel,
    group_service=Depends(create_group_service),
):
    response = group_service.create_group(group)

    return {"group_id": response.group_id}


@router.get("/organizations/{organizationId}/groups")
async def get_groups_by_organization(
    organization_id: UUID,
    group_service=Depends(create_group_service),
):
    response = group_service.get_all_for_organization(organization_id)
    #  проверить что если нет такой организации с чем упадем и заэксептить и вернуть 404
    return Response(response.json(), status_code=200)


@router.get("groups/{groupId}")
async def get_group(
    group_id: UUID,
    group_service=Depends(create_group_service),
):
    response = group_service.get_by_id(group_id)
    #  проверить что если нет такой организации с чем упадем и заэксептить и вернуть 404
    if not response:
        return Response("Group not found", status_code=404)

    return Response(response.json(), status_code=200)
