from datetime import date

from fastapi import Depends

from models.schedule import ScheduleModel, ScheduleModelResponse
from src.dependencies import create_schedule_service


async def create_lesson(
    schedule: ScheduleModel,
    schedule_service=Depends(create_schedule_service),
) -> None:
    schedule_service.create_schedule(schedule)
    if len(schedule.child_id) == 0:
        return
    schedule_service.create_child_schedule_pairs(
        schedule.schedule_id, schedule.child_id
    )


async def get_schedule_for_group(
    group_id: str,
    date_day: date,
    schedule_service=Depends(create_schedule_service),
) -> list[ScheduleModelResponse]:
    return schedule_service.get_for_children_by_time(
        group_id, date_day
    ) + schedule_service.get_for_group_by_time(group_id, date_day)
