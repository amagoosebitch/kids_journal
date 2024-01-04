from fastapi import Depends

from db.models.parents import ParentModel
from src.dependencies import create_parent_service


async def create_parent(
    parent: ParentModel,
    organization_service=Depends(create_parent_service),
) -> None:
    organization_service.create_parent(parent)


async def get_parent_by_tg_id(
    tg_id: str,
    organization_service=Depends(create_parent_service),
) -> ParentModel | None:
    return organization_service.get_by_tg_user_id(tg_id)
