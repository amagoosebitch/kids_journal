from __future__ import annotations

from uuid import UUID

from fastapi import Depends, Path

from models.user import UserModel, UserModelResponse
from src.dependencies import create_group_service, create_user_service


def create_employee(
    employee: UserModel,
    organization_id: str = Path(...),
    user_service=Depends(create_user_service),
    groups_service=Depends(create_group_service),
) -> None:
    user_service.create_user(employee)
    group_ids = [
        str(group.group_id)
        for group in groups_service.get_all_for_organization(organization_id)
    ]
    if group_ids:
        user_service.link_teacher_to_groups(group_ids, str(employee.user_id))
    # todo: link role


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


async def get_employees_for_organization(
    organization_id: str,
    employee_service=Depends(create_user_service),
) -> list[UserModelResponse]:
    return employee_service.get_by_organization_id(organization_id)


async def get_employees_organization_names_by_phone(
    phone: str,
    employee_service=Depends(create_user_service),
) -> list[str]:
    return employee_service.get_organization_name_by_phone(phone)
