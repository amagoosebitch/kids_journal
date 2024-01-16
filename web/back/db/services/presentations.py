from typing import Any

from models.presentations import PresentationModel


class PresentationService:
    def __init__(self, ydb_pool: Any, db_prefix: str):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def create_presentation(self, args_model: PresentationModel) -> None:
        args = args_model.model_dump(exclude_none=False, mode="json")

        def callee(session: Any):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO presentation ({keys}) VALUES
                    (
                        "{presentation_id}",
                        "{name}",
                        "{file_url}",
                        "{photo_url}",
                        "{description}"
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
        def callee(session: Any):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO subject_presentation ({keys}) VALUES ({values});
                """.format(
                    db_prefix=self._db_prefix,
                    keys="subject_id, presentation_id",
                    values=f"{subject_id}, {presentation_id}",
                ),
                commit_tx=True,
            ),

        return self._pool.retry_operation_sync(callee)

    def get_by_id(self, presentation_id: str) -> PresentationModel | None:
        def callee(session: Any):
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
