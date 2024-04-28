from __future__ import annotations

import json
from typing import Any

from models.user import UserModel, UserModelResponse
from models.role import Roles


class UserService:
    def __init__(self, ydb_pool: Any, db_prefix: str):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def create_user(self, args_model: UserModel) -> None:
        args = args_model.model_dump(exclude_none=False, mode="json")

        def callee(session: Any):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO user ({keys}) VALUES
                    (
                        "{user_id}",
                        "{name}",
                        "{first_name}",
                        "{last_name}",
                        "{email}",
                        "{gender}",
                        "{phone_number}",
                        "{tg_user_id}",
                    );
                """.format(
                    db_prefix=self._db_prefix,
                    keys=", ".join(args.keys()),
                    **args,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_by_tg_user_id(self, tg_user_id: str) -> UserModel | None:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM user
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

        rows[0]["group_ids"] = json.loads(rows[0]["group_ids"].replace("'", '"'))
        rows[0]["role_id"] = Roles[rows[0]["role_id"]].value
        return UserModel.model_validate(rows[0])

    def get_by_phone(self, phone_number: str) -> UserModel | None:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM user
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

        rows[0]["group_ids"] = json.loads(rows[0]["group_ids"].replace("'", '"'))
        rows[0]["role_id"] = Roles[rows[0]["role_id"]].value
        return UserModel.model_validate(rows[0])

    def set_telegram_id(self, phone_number: str, tg_user_id: str) -> None:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPDATE user
                SET tg_user_id = "{tg_user_id}"
                WHERE phone_number = "{phone_number}"
                """.format(
                    db_prefix=self._db_prefix,
                    phone_number=phone_number,
                    tg_user_id=tg_user_id,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def link_teacher_to_groups(self, group_ids: list[str], teacher_id: str):
        def callee(session: Any):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO group_teacher ({keys}) VALUES {values}
                """.format(
                    db_prefix=self._db_prefix,
                    keys="group_id, teacher_id",
                    values=", ".join(
                        [f'("{group_id}", "{teacher_id}")' for group_id in group_ids]
                    ),
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_by_organization_id(self, organization_id: str) -> list[UserModelResponse]:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT DISTINCT e.user_id, e.name, e.phone_number, e.role_id
                FROM user as e
                JOIN group_teacher as gt ON gt.teacher_id = e.user_id
                JOIN group as g ON g.group_id = gt.group_id
                JOIN organization as org ON org.organization_id = g.organization_id
                WHERE org.organization_id = "{organization_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    organization_id=organization_id,
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        if not rows:
            return []
        result = []

        for row in rows:
            result.append(
                UserModelResponse(
                    user_id=row["e.user_id"],
                    name=row["e.name"],
                    phone_number=row["e.phone_number"],
                )
            )
        return result

    def get_organization_name_by_phone(self, phone_number: str) -> str | None:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT distinct org.name
                FROM user as u
                JOIN group_teacher as gt ON gt.teacher_id = u.user_id
                JOIN group as g ON g.group_id = gt.group_id
                JOIN organization as org ON org.organization_id = g.organization_id
                WHERE u.phone_number = "{phone_number}"
                """.format(
                    db_prefix=self._db_prefix,
                    phone_number=phone_number,
                ),
                commit_tx=True,
            )

        return list(
            map(
                lambda x: x["org.name"], self._pool.retry_operation_sync(callee)[0].rows
            )
        )

    def get_parent_by_child_id(self, child_id: str) -> tuple[UserModel | None, UserModel | None] | None:
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
        print(rows)
        if not rows:
            return None
        if len(rows) == 1:
            return UserModel.model_validate(rows[0]), None
        return UserModel.model_validate(rows[0]), UserModel.model_validate(rows[1])


