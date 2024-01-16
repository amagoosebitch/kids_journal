from datetime import datetime
from uuid import UUID

from fastapi import Depends

from db.services.organization import OrganizationModel
from models.schedule import ScheduleModel
from src.dependencies import create_schedule_service


async def create_lesson(
    schedule: ScheduleModel,
    schedule_service=Depends(create_schedule_service),
) -> None:
    schedule_service.create_schedule(schedule)
    if len(schedule.child_ids) == 0:
        return
    schedule_service.create_child_schedule_pairs(
        schedule.schedule_id, schedule.child_ids
    )


async def get_schedule_for_group(
    group_id: UUID,
    date: datetime,
    schedule_service=Depends(create_schedule_service),
) -> list[OrganizationModel]:
    return schedule_service.get_for_children_by_time(
        group_id, date
    ) + schedule_service.get_for_group_by_time(group_id, date)
