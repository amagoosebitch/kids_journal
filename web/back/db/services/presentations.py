from __future__ import annotations

from typing import Any

import ydb

from models.presentations import PresentationModel


class PresentationService:
    def __init__(self, ydb_pool: ydb.SessionPool, db_prefix: str):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def create_presentation(self, args_model: PresentationModel) -> None:
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
                        "{photo_url}"
                    );
                """.format(
                    db_prefix=self._db_prefix,
                    keys=", ".join(args.keys()),
                    **args,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def create_subject_presentations_pair(self, subject_id: str, presentation_id: str):
        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO subject_presentation ({keys}) VALUES ({values});
                """.format(
                    db_prefix=self._db_prefix,
                    keys="subject_id, presentation_id",
                    values=f'"{subject_id}", "{presentation_id}"',
                ),
                commit_tx=True,
            ),

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
                SELECT distinct p.presentation_id, p.name, p.description, p.photo_url, p.file_url
                FROM presentation as p
                JOIN subject_presentation as sp ON sp.presentation_id = p.presentation_id
                WHERE sp.subject_id = "{subject_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    subject_id=subject_id,
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        if not rows:
            return None
        result = []
        for row in rows:
            result.append(
                PresentationModel(
                    presentation_id=row["p.presentation_id"],
                    name=row["p.name"],
                    description=row["p.description"],
                    photo_url=row["p.photo_url"],
                    file_url=row["p.file_url"],
                )
            )
        return result
