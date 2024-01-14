from typing import Any

from models.parents import ParentModel


class ParentService:
    def __init__(self, ydb_pool: Any, db_prefix: str):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def create_parent(self, args_model: ParentModel):
        args = args_model.model_dump(exclude_none=False, mode="json")

        def callee(session: Any):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO parent ({keys}) VALUES
                    (
                        "{parent_id}",
                        "{name}",
                        "{first_name}",
                        "{last_name}",
                        "{email}",
                        "{gender}",
                        "{phone_number}",
                        {freq_notifications},
                        "{tg_user_id}"
                    );
                """.format(
                    db_prefix=self._db_prefix,
                    keys=", ".join(args.keys()),
                    **args,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_by_tg_user_id(self, tg_user_id: str) -> ParentModel | None:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM parent
                WHERE tg_user_id = "{tg_user_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    tg_user_id=tg_user_id,
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        if not rows:
            return None
        return ParentModel.model_validate(rows[0])

    def get_by_child_id(self, child_id: str) -> tuple[ParentModel, ParentModel] | None:
        parent_columns = ", ".join(
            f"parent.{column} as {column}"
            for column in [
                "parent_id",
                "name",
                "first_name",
                "last_name",
                "email",
                "gender",
                "phone_number",
                "freq_notifications",
                "tg_user_id",
            ]
        )

        def callee_1(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT {parent_columns}
                FROM parent
                JOIN child on child.parent_1_id = parent.parent_id
                WHERE child_id = "{child_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    parent_columns=parent_columns,
                    child_id=child_id,
                ),
                commit_tx=True,
            )

        def callee_2(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT {parent_columns}
                FROM parent
                JOIN child on child.parent_2_id = parent.parent_id
                WHERE child_id = "{child_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    parent_columns=parent_columns,
                    child_id=child_id,
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee_1)[0].rows or []
        rows.extend(self._pool.retry_operation_sync(callee_2)[0].rows or [])
        if not rows:
            return None
        return ParentModel.model_validate(rows[0]), ParentModel.model_validate(rows[1])

    def get_by_phone(self, phone_number: str) -> ParentModel | None:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM parent
                WHERE phone_number = "{phone_number}"
                """.format(
                    db_prefix=self._db_prefix,
                    phone_number=phone_number,
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        if not rows:
            return None
        return ParentModel.model_validate(rows[0])

    def set_telegram_id(self, phone_number: str, tg_user_id: str) -> bool:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPDATE parent
                SET tg_user_id = "{tg_user_id}"
                WHERE phone_number = "{phone_number}"
                """.format(
                    db_prefix=self._db_prefix,
                    phone_number=phone_number,
                    tg_user_id=tg_user_id,
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows  # посмотреть так ли это
        if not rows:
            return False
        return True
