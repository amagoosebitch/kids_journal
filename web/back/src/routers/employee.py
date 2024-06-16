from __future__ import annotations

from uuid import UUID

from fastapi import Depends, Path

import models
from models.user import UserModel, UserModelResponse
from src.dependencies import create_group_service, create_user_service


async def upsert_employee(
    employee: UserModel,
    organization_id: str = Path(...),
    user_service=Depends(create_user_service),
    groups_service=Depends(create_group_service),
) -> None:
    user_service.upsert_user(employee)
    user_service.link_user_to_organization(
        organization_id=organization_id, user_id=employee.user_id
    )
    user_service.link_role(user_id=employee.user_id, role=models.Roles.EMPLOYEE)


async def link_employee_to_group(
    employee_id: str = Path(...),
    group_id: str = Path(...),
    user_service=Depends(create_user_service),
) -> None:
    user_service.link_teacher_to_group(teacher_id=employee_id, group_id=group_id)


async def unlink_group_from_employee(
    employee_id: str = Path(...),
    group_id: str = Path(...),
    user_service=Depends(create_user_service),
) -> None:
    user_service.unlink_group_from_teacher(teacher_id=employee_id, group_id=group_id)


async def get_groups_for_employee(
    employee_id: str = Path(...),
    user_service=Depends(create_user_service),
) -> list[str]:
    return user_service.get_groups_ids_by_teacher(teacher_id=employee_id)


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
    return employee_service.get_teachers_by_organization_id(organization_id)


async def get_employees_organization_names_by_phone(
    phone: str,
    employee_service=Depends(create_user_service),
) -> list[str]:
    return employee_service.get_organization_name_by_phone(phone)


async def delete_employee(
    employee_id: str, employee_service=Depends(create_user_service)
) -> None:
    return employee_service.delete_by_id(employee_id=employee_id)
