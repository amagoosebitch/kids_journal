from uuid import UUID

from fastapi import Depends

from db.services.groups import GroupModel, GroupService
from src.dependencies import create_group_service


async def add_group_to_organization(
    group: GroupModel,
    group_service: GroupService = Depends(create_group_service),
) -> None:
    group_service.create_group(group)


async def get_groups_by_organization(
    organization_id: UUID,
    group_service: GroupService = Depends(create_group_service),
) -> list[GroupModel]:
    return group_service.get_all_for_organization(organization_id)


async def get_group(
    group_id: UUID,
    group_service: GroupService = Depends(create_group_service),
) -> GroupModel | None:
    response = group_service.get_by_id(group_id)
    if not response:
        return None
    return response
