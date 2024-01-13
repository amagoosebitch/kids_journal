from typing import Any

from db.utils import _format_time
from models.child import ChildModel


class ChildService:
    def __init__(self, ydb_pool: Any, db_prefix: str):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def create_child(self, args_model: ChildModel) -> None:
        args = args_model.model_dump(exclude_none=False, mode="json")

        datetime_fields = [
            "birth_date",
            "start_education_date",
            "start_education_time",
            "end_education_time",
        ]
        for field in datetime_fields:
            args[field] = _format_time(args[field])

        def callee(session: Any):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO child ({keys}) VALUES
                    (
                        "{child_id}",
                        "{name}",
                        "{first_name}",
                        "{last_name}",
                        Datetime("{birth_date}"),
                        Datetime("{start_education_date}"),
                        Datetime("{start_education_time}"),
                        Datetime("{end_education_time}"),
                        "{gender}",
                        "{parent_1_id}",
                        "{parent_2_id}"
                    );
                """.format(
                    db_prefix=self._db_prefix,
                    keys=", ".join(args.keys()),
                    **args,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)
