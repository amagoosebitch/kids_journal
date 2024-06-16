from typing import Any

import ydb

from db.utils import _format_date_time, _format_date_time_to_date
from models.child import ChildModel


class ChildService:
    def __init__(self, ydb_pool: ydb.SessionPool, db_prefix: str):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def upsert_child(self, args_model: ChildModel) -> None:
        args = args_model.model_dump(exclude_none=False, mode="json")

        datetime_fields = [
            "birth_date",
            "start_education_date",
            "end_education_date",
        ]
        for field in datetime_fields:
            args[field] = _format_date_time_to_date(args[field])

        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO child ({keys}) VALUES
                    (
                        "{child_id}",
                        "{first_name}",
                        "{middle_name}",
                        "{last_name}",
                        {birth_date},
                        {start_education_date},
                        {end_education_date},
                        "{gender}",
                        "{avatar_url}"
                    );
                """.format(
                    db_prefix=self._db_prefix,
                    keys=", ".join(args.keys()),
                    **args,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def link_to_group(self, group_id: str, child_id: str) -> None:
        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO group_child {keys} VALUES {values}
                """.format(
                    db_prefix=self._db_prefix,
                    keys="(group_id, child_id)",
                    values=f'("{group_id}", "{child_id}")',
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def unlink_from_groups(self, child_id: str):
        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                DELETE FROM group_child
                WHERE child_id = "{child_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    child_id=child_id,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_child_by_id(self, child_id: str):
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM child
                WHERE id = "{child_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    child_id=child_id,
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        if not rows:
            return None
        if len(rows) > 1:
            raise ValueError("Duplicated id in db table")
        return ChildModel.model_validate(rows[0])

    def delete_by_id(self, child_id: str):
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                delete
                FROM child
                WHERE child_id = "{child_id}"
                """.format(
                    db_prefix=self._db_prefix, child_id=child_id
                ),
                commit_tx=True,
            )

        self._pool.retry_operation_sync(callee)
