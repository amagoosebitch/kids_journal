from __future__ import annotations

from datetime import date, timedelta
from itertools import groupby
from typing import Any

import ydb

from db.utils import _format_date_time
from models.schedule import ScheduleModel, ScheduleModelResponse


class ScheduleService:
    def __init__(self, ydb_pool: ydb.SessionPool, db_prefix: str):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def upsert_schedule(self, args_model: ScheduleModel) -> None:
        args = args_model.model_dump(
            exclude_none=False, mode="json", exclude={"child_id"}
        )

        datetime_fields = [
            "start_lesson",
            "end_lesson",
        ]
        for field in datetime_fields:
            args[field] = _format_date_time(args[field])
        args["canceled"] = str(args_model.canceled).lower()

        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO schedule ({keys}) VALUES
                    (
                        "{schedule_id}",
                        "{presentation_id}",
                        {start_lesson},
                        {end_lesson},
                        {canceled}
                    );
                """.format(
                    db_prefix=self._db_prefix,
                    keys=", ".join(args.keys()),
                    **args,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def create_child_schedule_pairs(
        self, schedule_id: str, child_ids: list[str]
    ) -> None:
        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO child_schedule ({keys}) VALUES {values};
                """.format(
                    db_prefix=self._db_prefix,
                    keys="child_id, schedule_id",
                    values=", ".join(
                        [f'("{child_id}", "{schedule_id}")' for child_id in child_ids]
                    ),
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def create_group_schedule_pair(self, schedule_id: str, group_id: str) -> None:
        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO group_schedule ({keys}) VALUES {values};
                """.format(
                    db_prefix=self._db_prefix,
                    keys="group_id, schedule_id",
                    values=f'("{group_id}", "{schedule_id}")',
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def remove_all_group_pairs(self, schedule_id: str) -> None:
        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                DELETE FROM group_schedule
                WHERE schedule_id = "{schedule_id}";
                """.format(
                    db_prefix=self._db_prefix,
                    schedule_id=schedule_id,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def remove_all_child_pairs(self, schedule_id: str) -> None:
        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                DELETE FROM child_schedule
                WHERE schedule_id = "{schedule_id}";
                """.format(
                    db_prefix=self._db_prefix,
                    schedule_id=schedule_id,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def unlink_schedule_from_child(self, schedule_id: str, child_id: str) -> None:
        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                DELETE FROM child_schedule
                WHERE schedule_id = "{schedule_id}" AND child_id = "{child_id}";
                """.format(
                    db_prefix=self._db_prefix,
                    schedule_id=schedule_id,
                    child_id=child_id,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_for_child_by_date(
        self, child_id: str, date_day: date
    ) -> list[ScheduleModelResponse] | None:
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT DISTINCT cs.schedule_id, s.start_lesson, s.presentation_id
                FROM child_schedule as cs
                JOIN schedule as s ON cs.schedule_id = s.schedule_id 
                WHERE cs.child_id = "{child_id}" AND s.start_lesson >= {date_str_start} AND s.start_lesson < {date_str_end}
                """.format(
                    db_prefix=self._db_prefix,
                    child_id=child_id,
                    date_str_end=self._get_time_str(date_day, timedelta(days=1)),
                    date_str_start=self._get_time_str(date_day, timedelta(days=0)),
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        result = []
        if not rows:
            return result
        for row in rows:
            result.append(
                ScheduleModelResponse(
                    schedule_id=row["cs.schedule_id"],
                    date_day=date_day,
                    presentation_id=row["s.presentation_id"],
                    is_for_child=True,
                )
            )
        return result

    def get_for_group_by_date(
        self, group_id: str, date_day: date
    ) -> list[ScheduleModelResponse] | None:
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT s.schedule_id, s.presentation_id, s.start_lesson
                FROM schedule as s
                JOIN group_schedule as gs ON gs.schedule_id = s.schedule_id
                JOIN group as g ON g.group_id = gs.group_id
                WHERE gs.group_id = "{group_id}" AND s.start_lesson > {date_str_start} AND s.start_lesson < {date_str_end} 
                """.format(
                    db_prefix=self._db_prefix,
                    group_id=group_id,
                    date_str_end=self._get_time_str(date_day, timedelta(days=1)),
                    date_str_start=self._get_time_str(date_day, timedelta(days=0)),
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        result = []
        if not rows:
            return result
        for row in rows:
            result.append(
                ScheduleModelResponse(
                    schedule_id=row["s.schedule_id"],
                    is_for_child=False,
                    date_day=date_day,
                    presentation_id=row["s.presentation_id"],
                )
            )
        return result

    @classmethod
    def _get_time_str(cls, date_day: date, delta: timedelta) -> str:
        return _format_date_time(str(date_day + delta))

    def delete_by_id(self, schedule_id: str):
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                delete
                FROM schedule
                WHERE schedule_id = "{schedule_id}"
                """.format(
                    db_prefix=self._db_prefix, schedule_id=schedule_id
                ),
                commit_tx=True,
            )

        self._pool.retry_operation_sync(callee)
