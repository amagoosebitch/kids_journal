from __future__ import annotations

from fastapi import Depends, Path

from models.user import UserModel
from src.dependencies import create_user_service


async def create_parent(
    parent: UserModel,
    user_service=Depends(create_user_service),
) -> None:
    user_service.create_user(parent)
    # todo: link role


async def get_parent_by_tg_id(
    tg_id: str,
    user_service=Depends(create_user_service),
) -> UserModel | None:
    return user_service.get_by_tg_user_id(tg_id)


async def get_parents_by_child_id(
    child_id: str,
    user_service=Depends(create_user_service),
) -> tuple[UserModel | None, UserModel | None] | None:
    return user_service.get_parent_by_child_id(child_id)
