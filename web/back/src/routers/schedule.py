from __future__ import annotations

from datetime import date

from fastapi import Depends

from models.schedule import ScheduleModel, ScheduleModelResponse
from src.dependencies import create_schedule_service


async def upsert_lesson(
    schedule: ScheduleModel,
    group_id: str | None,
    child_ids: str | None,
    schedule_service=Depends(create_schedule_service),
) -> None:
    schedule_service.upsert_schedule(schedule)
    if child_ids:
        schedule_service.remove_all_child_pairs(schedule.schedule_id)
        schedule_service.create_child_schedule_pairs(
            schedule.schedule_id, child_ids
        )
    if group_id:
        schedule_service.remove_all_group_pairs(schedule.schedule_id)
        schedule_service.create_group_schedule_pair(
            schedule.schedule_id, group_id
        )


async def get_schedule_for_group(
    group_id: str,
    date_day: date,
    schedule_service=Depends(create_schedule_service),
) -> list[ScheduleModelResponse]:
    return schedule_service.get_for_group_by_time(group_id, date_day)


async def get_schedule_for_child(
    child_id: str,
    date_day: date,
    schedule_service=Depends(create_schedule_service),
) -> list[ScheduleModelResponse]:
    return schedule_service.get_for_child_by_time(child_id, date_day)


