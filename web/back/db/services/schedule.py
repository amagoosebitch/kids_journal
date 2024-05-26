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

    def create_schedule(self, args_model: ScheduleModel) -> None:
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

    def get_for_children_by_time(
        self, group_id: str, date_day: date
    ) -> list[ScheduleModelResponse] | None:
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT DISTINCT ch.name, ch.child_id, s.schedule_id, s.start_lesson
                FROM schedule as s
                JOIN child_schedule as cs on cs.schedule_id = s.schedule_id
                JOIN child as ch on cs.child_id = ch.child_id
                WHERE s.start_lesson > {date_str_start} AND s.start_lesson < {date_str_end} AND s.group_id = "{group_id}"
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
        for key, group in groupby(rows, lambda x: x["s.schedule_id"]):
            child_ids = set()
            for row in group:
                if row["ch.child_id"] in child_ids:
                    continue
                child_ids.add(row["ch.child_id"])
            result.append(
                ScheduleModelResponse(
                    schedule_id=key,
                    child_ids=list(child_ids),
                    is_for_child=True,
                    # subject_name=row["su.name"],
                    # description=row["s.description"],
                    date_day=row["s.start_lesson"],
                    # group_name=row["s.group_id"],
                    # presentation_id=row["s.presentation_id"],
                )
            )
        return result

    def get_for_group_by_time(
        self, group_id: str, date_day: date
    ) -> list[ScheduleModelResponse] | None:
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT su.name, g.name, s.description, s.schedule_id, s.presentation_id, s.start_lesson
                FROM schedule as s
                left JOIN child_schedule as cs on cs.schedule_id = s.schedule_id
                JOIN group_schedule as gs ON gs.group_id = s.group_id
                JOIN group as g ON g.group_id = gs.group_id
                JOIN subject as su ON s.subject_id = su.subject_id
                WHERE s.start_lesson > {date_str_start} AND s.start_lesson < {date_str_end} AND s.group_id = "{group_id}" AND cs.child_id is null
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
                    subject_name=row["su.name"],
                    description=row["s.description"],
                    date_day=row["s.start_lesson"],
                    group_name=row["g.name"],
                    presentation_id=row["s.presentation_id"],
                )
            )
        return result

    @classmethod
    def _get_time_str(cls, date_day: date, delta: timedelta) -> str:
        return _format_date_time(str(date_day + delta))
