import json
from datetime import datetime, timedelta
from typing import Any

from db.utils import _format_time
from models.schedule import ScheduleModel, ScheduleModelResponse


class ScheduleService:
    def __init__(self, ydb_pool: Any, db_prefix: str):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def create_schedule(self, args_model: ScheduleModel) -> None:
        args = args_model.model_dump(exclude_none=False, mode="json", exclude={'child_id'})

        datetime_fields = [
            "start_lesson",
            "end_lesson",
        ]
        for field in datetime_fields:
            args[field] = _format_time(args[field])

        def callee(session: Any):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO schedule ({keys}) VALUES
                    (
                        "{schedule_id}",
                        "{group_id}",
                        Datetime("{start_lesson}"),
                        Datetime("{end_lesson}"),
                        "{description}",
                        "{teacher_id}",
                        "{subject_id}",
                        "{presentation_id}",
                        "{note_id}",
                        "canceled",
                    );
                """.format(
                    db_prefix=self._db_prefix,
                    keys=", ".join(args.keys()),
                    **args,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def create_child_schedule_pairs(self, schedule_id: str, child_ids: list[str]) -> None:
        def callee(session: Any):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO child_schedule ({keys}) VALUES {values};
                """.format(
                    db_prefix=self._db_prefix,
                    keys="child_id, schedule_id",
                    values=", ".join([f"({child_id}, {schedule_id}), " for child_id in child_ids]),
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_for_children_by_time(self, group_id: str, date: datetime) -> list[ScheduleModelResponse] | None:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT ch.name, su.name, s.description
                FROM schedule as s
                JOIN group as g ON g.group_id = s.group_id
                JOIN group_child as gc on g.group_id = gc.group_id
                JOIN child as ch on gc.child_id = ch.child_id
                JOIN subject as su ON s.subject_id = su.subject_id
                WHERE s.end_lesson < Datetime("{date_str}") AND s.group_id = "{group_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    group_id=group_id,
                    date_str=self._get_time_str(date),
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        if not rows:
            return None
        return ScheduleModelResponse.model_validate(rows[0])

    def get_for_group_by_time(self, group_id: str, date: datetime, child_ids: list[str]) -> list[ScheduleModelResponse] | None:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT su.name, g.name, s.description
                FROM schedule as s
                JOIN group as g ON g.group_id = s.group_id
                JOIN subject as su ON s.subject_id = su.subject_id
                WHERE s.end_lesson < Datetime("{date_str}") AND s.group_id = "{group_id}" AND s.child_id NOT IN ({child_ids})
                """.format(
                    db_prefix=self._db_prefix,
                    group_id=group_id,
                    date_str=self._get_time_str(date),
                    child_ids=", ".join(f'"{child_id}"' for child_id in child_ids),
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        if not rows:
            return None
        return ScheduleModelResponse.model_validate(rows[0])

    @classmethod
    def _get_time_str(cls, date: datetime) -> str:
        date = (date.date() + timedelta(days=1))
        return _format_time(str(date))
