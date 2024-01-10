from fastapi import Depends

from db.models.child import ChildModel
from src.dependencies import create_child_service


async def create_child(
    employee: ChildModel,
    organization_service=Depends(create_child_service),
) -> None:
    organization_service.create_child(employee)
