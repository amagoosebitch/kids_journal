from __future__ import annotations

import ydb

from models.skills import ChildSkillModel, SkillLevelModel, SkillModel


class SkillService:
    def __init__(self, ydb_pool: ydb.SessionPool, db_prefix: str):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def upsert_skill_level(self, args_model: SkillLevelModel) -> None:
        args = args_model.model_dump(exclude_none=False, mode="json")

        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO skill_level ({keys}) VALUES
                    (
                        "{skill_level_id}",
                        "{name}",
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

    def get_skill_level_by_id(self, skill_level_id: str) -> SkillLevelModel | None:
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM skill_level
                WHERE skill_level_id = "{skill_level_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    skill_level_id=skill_level_id,
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        if not rows:
            return None
        return SkillLevelModel.model_validate(rows[0])

    def get_all_skill_levels(self) -> list[SkillLevelModel] | None:
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM skill_level
                """.format(
                    db_prefix=self._db_prefix,
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        if not rows:
            return None
        return [SkillLevelModel.model_validate(rows[i]) for i in range(len(rows))]

    def link_to_child(self, presentation_id, child_id, skill_level_id) -> None:
        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO child_skills {keys} VALUES {values}
                """.format(
                    db_prefix=self._db_prefix,
                    keys="(child_id, presentation_id, skill_level_id)",
                    values=f'("{child_id}", "{presentation_id}", "{skill_level_id}")',
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def unlink_from_child(self, presentation_id, child_id) -> None:
        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                DELETE FROM child_skills
                WHERE child_id = "{child_id}" AND presentation_id = "{presentation_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    child_id=child_id,
                    presentation_id=presentation_id,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_all_skills_for_child(self, child_id: str) -> list[ChildSkillModel] | None:
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT * FROM child_skills
                WHERE child_id = "{child_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    child_id=child_id,
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        if not rows:
            return None
        return [ChildSkillModel.model_validate(rows[i]) for i in range(len(rows))]

    def delete_by_id(self, skill_level_id: str) -> None:
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                delete
                FROM skill_level
                WHERE skill_level_id = "{skill_level_id}"
                """.format(
                    db_prefix=self._db_prefix, skill_level_id=skill_level_id
                ),
                commit_tx=True,
            )

        self._pool.retry_operation_sync(callee)
