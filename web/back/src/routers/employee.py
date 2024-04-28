from uuid import UUID

from fastapi import Depends, Path

from models.user import UserModel, EmployeeResponse
from src.dependencies import create_employee_service, create_group_service


def create_employee(
    employee: UserModel,
    organization_id: str = Path(...),
    employee_service=Depends(create_employee_service),
    groups_service=Depends(create_group_service),
) -> None:
    employee_service.create_employee(employee)
    group_ids = [
        str(group.group_id)
        for group in groups_service.get_all_for_organization(organization_id)
    ]
    if group_ids:
        employee_service.link_to_groups(group_ids, str(employee.employee_id))


async def get_employee_by_tg_id(
    tg_id: str,
    employee_service=Depends(create_employee_service),
) -> UserModel | None:
    return employee_service.get_by_tg_user_id(tg_id)


async def get_employee_by_phone(
    phone: str,
    employee_service=Depends(create_employee_service),
) -> UserModel | None:
    return employee_service.get_by_phone(phone)


async def get_employees_for_organization(
    organization_id: str,
    employee_service=Depends(create_employee_service),
) -> list[EmployeeResponse]:
    return employee_service.get_by_organization_id(organization_id)


async def get_employees_organization_names_by_phone(
    phone: str,
    employee_service=Depends(create_employee_service),
) -> list[str]:
    return employee_service.get_organization_name_by_phone(phone)
