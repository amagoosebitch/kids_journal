from fastapi import Depends

from db.services.employee import EmployeeService
from db.services.parent import ParentService
from models.user import MergeUserModel, UserModelResponse, UserRole
from src.dependencies import create_employee_service, create_parent_service


async def try_merge_user_by_phone(
    user: MergeUserModel,
    employee_service: EmployeeService = Depends(create_employee_service),
    parent_service: ParentService = Depends(create_parent_service),
) -> UserModelResponse:
    unknown_user = UserModelResponse(role=UserRole.UNKNOWN)
    employee = employee_service.get_by_phone(user.phone_number)
    if employee is not None:
        success = employee_service.set_telegram_id(user.phone_number, user.tg_user_id)
        if success:
            return UserModelResponse(role=UserRole.EMPLOYEE, data=employee)
        return unknown_user
    parent = parent_service.get_by_phone(user.phone_number)
    if parent is not None:
        success = parent_service.set_telegram_id(user.phone_number, user.tg_user_id)
        if success:
            return UserModelResponse(role=UserRole.PARENT, data=parent)
        return unknown_user
    return unknown_user
