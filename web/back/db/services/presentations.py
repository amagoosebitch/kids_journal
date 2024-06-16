from __future__ import annotations

from typing import Any

import ydb

from models.presentations import PresentationModel


class PresentationService:
    def __init__(self, ydb_pool: ydb.SessionPool, db_prefix: str):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def upsert_presentation(self, args_model: PresentationModel) -> None:
        args = args_model.model_dump(exclude_none=False, mode="json")

        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO presentation ({keys}) VALUES
                    (
                        "{presentation_id}",
                        "{name}",
                        "{description}",
                        "{file_url}",
                        "{photo_url}",
                        "{subject_id}"
                    );
                """.format(
                    db_prefix=self._db_prefix,
                    keys=", ".join(args.keys()),
                    **args,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_by_id(self, presentation_id: str) -> PresentationModel | None:
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM presentation
                WHERE presentation_id = "{presentation_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    presentation_id=presentation_id,
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        if not rows:
            return None
        return PresentationModel.model_validate(rows[0])

    def get_all_for_subject(self, subject_id: str) -> list[PresentationModel] | None:
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT distinct presentation_id, name, description, photo_url, file_url, subject_id
                FROM presentation
                WHERE subject_id = "{subject_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    subject_id=subject_id,
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        result = self._make_result_from_rows(rows)
        return result

    def _make_result_from_rows(
        self, rows: list[dict]
    ) -> list[PresentationModel] | None:
        if not rows:
            return None
        result = []
        for row in rows:
            result.append(
                PresentationModel(
                    presentation_id=row["presentation_id"],
                    name=row["name"],
                    description=row["description"],
                    photo_url=row["photo_url"],
                    file_url=row["file_url"],
                    subject_id=row["subject_id"],
                )
            )
        return result

    def delete_by_id(self, presentation_id: str) -> None:
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                delete
                FROM presentation
                WHERE presentation_id = "{presentation_id}"
                """.format(
                    db_prefix=self._db_prefix, presentation_id=presentation_id
                ),
                commit_tx=True,
            )

        self._pool.retry_operation_sync(callee)
