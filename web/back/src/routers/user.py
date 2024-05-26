from fastapi import Depends

from db.services.user import UserService
from models.role import UserRole, UserRoleResponse
from models.user import MergeUserModel
from src.dependencies import create_user_service


async def try_merge_user_by_phone(
    user: MergeUserModel,
    employee_service: UserService = Depends(create_user_service),
    parent_service: UserService = Depends(create_user_service),
) -> UserRoleResponse:
    unknown_user = UserRoleResponse(role=UserRole.UNKNOWN)
    employee = employee_service.get_by_phone(user.phone_number)
    if employee is not None:
        employee_service.set_telegram_id(user.phone_number, user.tg_user_id)
        return UserRoleResponse(role=UserRole.EMPLOYEE, data=employee)
    parent = parent_service.get_by_phone(user.phone_number)
    if parent is not None:
        parent_service.set_telegram_id(user.phone_number, user.tg_user_id)
        return UserRoleResponse(role=UserRole.PARENT, data=parent)
    return unknown_user
