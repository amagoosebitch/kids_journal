from fastapi import Depends

from db.models.employees import EmployeeModel
from src.dependencies import create_employee_service


async def create_employee(
    employee: EmployeeModel,
    organization_service=Depends(create_employee_service),
) -> None:
    organization_service.create_employee(employee)


async def get_employee_by_tg_id(
    tg_id: str,
    organization_service=Depends(create_employee_service),
) -> EmployeeModel | None:
    return organization_service.get_by_tg_user_id(tg_id)
