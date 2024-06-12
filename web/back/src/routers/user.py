from __future__ import annotations

from fastapi import Depends

from db.services.user import UserService
from models.role import Roles, UserRoleResponse
from models.user import MergeUserModel, UserModel
from src.dependencies import create_user_service


async def try_merge_user_by_phone(
    user: MergeUserModel,
    employee_service: UserService = Depends(create_user_service),
    parent_service: UserService = Depends(create_user_service),
) -> UserRoleResponse:
    unknown_user = UserRoleResponse(role=Roles.UNKNOWN)
    employee = employee_service.get_by_phone(user.phone_number)
    if employee is not None:
        employee_service.set_telegram_id(user.phone_number, user.tg_user_id)
        return UserRoleResponse(role=Roles.EMPLOYEE, data=employee)
    parent = parent_service.get_by_phone(user.phone_number)
    if parent is not None:
        parent_service.set_telegram_id(user.phone_number, user.tg_user_id)
        return UserRoleResponse(role=Roles.PARENT, data=parent)
    return unknown_user


async def get_user_by_tg_id(
    tg_id: str,
    user_service=Depends(create_user_service),
) -> UserModel | None:
    return user_service.get_by_tg_user_id(tg_id)


async def get_user_by_phone(
    phone: str,
    user_service=Depends(create_user_service),
) -> UserModel | None:
    return user_service.get_by_phone(phone)


async def get_user_by_id(
    user_id: str,
    user_service=Depends(create_user_service),
) -> UserModel | None:
    return user_service.get_by_user_id(user_id)
