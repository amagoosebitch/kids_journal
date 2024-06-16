from __future__ import annotations

from typing import Any

import ydb

from models.subjects import SubjectModel


class SubjectService:
    def __init__(self, ydb_pool: ydb.SessionPool, db_prefix: str):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def create_subject(self, args_model: SubjectModel) -> None:
        args = args_model.model_dump(
            exclude_none=False, mode="json", exclude={"presentations"}
        )

        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO subject ({keys}) VALUES
                    (
                        "{subject_id}",
                        "{name}",
                        "{description}",
                        "{age_range}"
                    )
                """.format(
                    db_prefix=self._db_prefix,
                    keys=", ".join(args.keys()),
                    **args,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def create_group_subject_pair(self, group_ids: list[str], subject_id: str):
        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO group_subject ({keys}) VALUES {values}
                """.format(
                    db_prefix=self._db_prefix,
                    keys="group_id, subject_id",
                    values=", ".join(
                        [f'("{group_id}", "{subject_id}")' for group_id in group_ids]
                    ),
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_by_id(self, subject_id: str) -> SubjectModel | None:
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM subject
                WHERE subject_id = "{subject_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    subject_id=subject_id,
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        if not rows:
            return None

        return SubjectModel.model_validate(rows[0])

    def get_all(self) -> list[SubjectModel]:
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM subject
                """.format(
                    db_prefix=self._db_prefix,
                ),
                commit_tx=True,
            )

        results = self._pool.retry_operation_sync(callee)[0].rows
        return [SubjectModel.model_validate(result) for result in results]

    def delete_by_id(self, subject_id: str) -> None:
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                delete
                FROM subject
                WHERE subject_id = "{subject_id}"
                """.format(
                    db_prefix=self._db_prefix, subject_id=subject_id
                ),
                commit_tx=True,
            )

        self._pool.retry_operation_sync(callee)
