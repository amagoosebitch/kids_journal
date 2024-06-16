from __future__ import annotations

from uuid import UUID

from fastapi import Depends

from models.child import ChildModel
from src.dependencies import create_child_service


async def upsert_child(
    child: ChildModel,
    group_id: str | None,
    child_service=Depends(create_child_service),
) -> None:
    child_service.upsert_child(child)
    if group_id:
        child_service.unlink_from_groups(child.child_id)
        child_service.link_to_group(group_id, child.child_id)


async def delete_child(
    child_id: str, child_service=Depends(create_child_service)
) -> None:
    return child_service.delete_by_id(child_id=child_id)
