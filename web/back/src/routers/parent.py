from __future__ import annotations

from fastapi import Depends, Path

import models
from models.user import UserModel
from src.dependencies import create_user_service


async def create_parent(
    parent: UserModel,
    user_service=Depends(create_user_service),
) -> None:
    user_service.upsert_user(parent)
    user_service.link_role(user_id=parent.user_id, role=models.Roles.PARENT)


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


async def delete_parent(
    parent_id: str,
    user_service=Depends(create_user_service),
) -> None:
    return user_service.delete_by_id(user_id=parent_id)
