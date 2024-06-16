from __future__ import annotations

import uuid
from datetime import date

from fastapi import Depends, Path

from models.schedule import ScheduleModel, ScheduleModelResponse
from src.dependencies import create_schedule_service


async def upsert_lesson(
    schedule: ScheduleModel,
    group_id: str | None = None,
    child_ids: list[str] | None = None,
    schedule_service=Depends(create_schedule_service),
) -> None:
    schedule_service.upsert_schedule(schedule)
    if child_ids:
        schedule_service.remove_all_child_pairs(schedule.schedule_id)
        schedule_service.create_child_schedule_pairs(schedule.schedule_id, child_ids)
    if group_id:
        schedule_service.remove_all_group_pairs(schedule.schedule_id)
        schedule_service.create_group_schedule_pair(schedule.schedule_id, group_id)


async def get_schedule_for_group(
    group_id: str,
    date_day: date,
    schedule_service=Depends(create_schedule_service),
) -> list[ScheduleModelResponse]:
    return schedule_service.get_for_group_by_date(group_id, date_day)


async def get_schedule_for_child_by_date(
    date_day: date,
    child_id: str = Path(...),
    schedule_service=Depends(create_schedule_service),
) -> list[ScheduleModelResponse]:
    return schedule_service.get_for_child_by_date(child_id, date_day)


async def unlink_lesson_from_child(
    schedule_id: str,
    child_id: str,
    schedule_service=Depends(create_schedule_service),
) -> None:
    schedule_service.unlink_schedule_from_child(
        schedule_id=schedule_id, child_id=child_id
    )


async def delete_lesson(
    schedule_id: str, schedule_service=Depends(create_schedule_service)
) -> None:
    schedule_service.delete_by_id(schedule_id=schedule_id)
    schedule_service.remove_all_child_pairs(schedule_id)
    schedule_service.remove_all_group_pairs(schedule_id)
