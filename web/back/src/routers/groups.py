from uuid import UUID

from fastapi import Depends
from starlette.responses import Response

from db.services.groups import GroupModel, GroupService
from src.dependencies import create_group_service


async def add_group_to_organization(
    group: GroupModel,
    group_service: GroupService = Depends(create_group_service),
):
    group_service.create_group(group)


async def get_groups_by_organization(
    organization_id: UUID,
    group_service: GroupService = Depends(create_group_service),
):
    response = group_service.get_all_for_organization(organization_id)
    #  проверить что если нет такой организации с чем упадем и заэксептить и вернуть 404
    return Response(response.json(), status_code=200)


async def get_group(
    group_id: UUID,
    group_service: GroupService = Depends(create_group_service),
):
    response = group_service.get_by_id(group_id)
    if not response:
        return Response("Group not found", status_code=404)

    return Response(response.model_dump_json(), status_code=200)
