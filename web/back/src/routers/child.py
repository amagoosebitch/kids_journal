from uuid import UUID

from fastapi import Depends

from models.child import ChildModel
from src.dependencies import create_child_service


async def create_child(
    child: ChildModel,
    group_id: str,
    child_service=Depends(create_child_service),
) -> None:
    child_service.create_child(child)
    child_service.link_to_group(group_id, child.child_id)
