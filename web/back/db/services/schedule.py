from datetime import datetime, timedelta
from itertools import groupby
from typing import Any

from db.utils import _format_date_time
from models.schedule import ScheduleModel, ScheduleModelResponse


class ScheduleService:
    def __init__(self, ydb_pool: Any, db_prefix: str):
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

        def callee(session: Any):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO schedule ({keys}) VALUES
                    (
                        "{schedule_id}",
                        "{group_id}",
                        "{teacher_id}",
                        "{subject_id}",
                        "{presentation_id}",
                        {start_lesson},
                        {end_lesson},
                        "{description}",
                        "{note_id}",
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
        def callee(session: Any):
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
        self, group_id: str, date: datetime
    ) -> list[ScheduleModelResponse] | None:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT ch.name, ch.child_id, su.name, s.description, s.schedule_id
                FROM schedule as s
                JOIN child_schedule as cs on cs.schedule_id = s.schedule_id
                JOIN child as ch on cs.child_id = ch.child_id
                JOIN subject as su ON s.subject_id = su.subject_id
                WHERE s.end_lesson < {date_str} AND s.group_id = "{group_id}"
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
        result = []
        child_ids = set()
        for key, group in groupby(rows, lambda x: x["s.schedule_id"]):
            child_names = []
            for row in group:
                child_names.append(row["ch.name"])
                child_ids.add(row["ch.child_id"])
            result.append(
                ScheduleModelResponse(
                    schedule_id=key,
                    child_names=child_names,
                    is_for_child=True,
                    subject_name=row["su.name"],
                    description=row["s.description"],
                    date=date,
                    group_name=row["g.name"],
                )
            )
        return result

    def get_for_group_by_time(
        self, group_id: str, date: datetime
    ) -> list[ScheduleModelResponse] | None:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT su.name, g.name, s.description, s.schedule_id
                FROM schedule as s
                left JOIN child_schedule as cs on cs.schedule_id = s.schedule_id
                JOIN group as g ON g.group_id = s.group_id
                JOIN group_child as gc on gc.group_id = g.group_id
                JOIN subject as su ON s.subject_id = su.subject_id
                WHERE s.end_lesson < {date_str} AND s.group_id = "{group_id}"./src/routers/presentation.py AND cs.child_id is null
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
        result = []
        for row in rows:
            result.append(
                ScheduleModelResponse(
                    schedule_id=row["s.schedule_id"],
                    is_for_child=False,
                    subject_name=row["su.name"],
                    description=row["s.description"],
                    date=date,
                    group_name=row["g.name"],
                )
            )
        return result

    @classmethod
    def _get_time_str(cls, date: datetime) -> str:
        date = date.date() + timedelta(days=1)
        return _format_date_time(str(date))
