from fastapi import Depends

from models.user import UserModel
from src.dependencies import create_parent_service


async def create_parent(
    parent: UserModel,
    organization_service=Depends(create_parent_service),
) -> None:
    organization_service.create_parent(parent)


async def get_parent_by_tg_id(
    tg_id: str,
    organization_service=Depends(create_parent_service),
) -> UserModel | None:
    return organization_service.get_by_tg_user_id(tg_id)


async def get_parents_by_child_id(
    child_id: str,
    organization_service=Depends(create_parent_service),
) -> tuple[UserModel | None, UserModel | None] | None:
    return organization_service.get_by_child_id(child_id)
