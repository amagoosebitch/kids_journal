from uuid import UUID

from fastapi import Depends

from models.employees import EmployeeModel
from src.dependencies import create_employee_service, create_group_service


def create_employee(
    employee: EmployeeModel,
    organization_id: UUID,
    organization_service=Depends(create_employee_service),
    groups_service=Depends(create_group_service),
) -> None:
    organization_service.create_employee(employee)
    group_ids = [
        str(group.group_id)
        for group in groups_service.get_all_for_organization(organization_id)
    ]
    organization_service.link_to_groups(group_ids, str(employee.employee_id))


async def get_employee_by_tg_id(
    tg_id: str,
    organization_service=Depends(create_employee_service),
) -> EmployeeModel | None:
    return organization_service.get_by_tg_user_id(tg_id)
