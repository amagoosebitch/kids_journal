from __future__ import annotations

import json
from typing import Any

import ydb

import models.role
from models.user import UserModel, UserModelResponse


class UserService:
    def __init__(self, ydb_pool: ydb.SessionPool, db_prefix: str):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def upsert_user(self, args_model: UserModel) -> None:
        args = args_model.model_dump(exclude_none=False, mode="json")

        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO user ({keys}) VALUES
                    (
                        "{user_id}",
                        "{first_name}",
                        "{middle_name}",
                        "{last_name}",
                        "{email}",
                        "{gender}",
                        "{phone_number}",
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

    def link_user_to_organization(self, organization_id: str, user_id: str) -> None:
        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO organizations_users (organization_id, user_id) VALUES
                    (
                        "{organization_id}",
                        "{user_id}"
                    );
                """.format(
                    db_prefix=self._db_prefix,
                    organization_id=organization_id,
                    user_id=user_id,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_by_tg_user_id(self, tg_user_id: str) -> UserModel | None:
        def callee(session: ydb.Session):
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

        return UserModel.model_validate(rows[0])

    def get_by_phone(self, phone_number: str) -> UserModel | None:
        def callee(session: ydb.Session):
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

        return UserModel.model_validate(rows[0])

    def set_telegram_id(self, phone_number: str, tg_user_id: str) -> None:
        def callee(session: ydb.Session):
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

    def link_teacher_to_group(self, group_id: str, teacher_id: str):
        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO group_teacher ({keys}) VALUES {values}
                """.format(
                    db_prefix=self._db_prefix,
                    keys="group_id, teacher_id",
                    values=f'("{group_id}", "{teacher_id}")',
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def unlink_group_from_teacher(self, group_id: str, teacher_id: str):
        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                DELETE FROM group_teacher
                WHERE teacher_id = "{teacher_id}" AND group_id = "{group_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    teacher_id=teacher_id,
                    group_id=group_id,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_groups_ids_by_teacher(self, teacher_id: str) -> list[str]:
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT group_id
                FROM group_teacher
                WHERE teacher_id = "{teacher_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    teacher_id=teacher_id,
                ),
                commit_tx=True,
            )

        return list(
            map(
                lambda x: x["group_id"], self._pool.retry_operation_sync(callee)[0].rows
            )
        )

    def get_teachers_by_organization_id(
        self, organization_id: str
    ) -> list[UserModelResponse]:
        def callee(session: ydb.Session):
            # todo fix role
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT DISTINCT u.user_id, u.first_name, u.last_name, u.phone_number
                FROM user as u
                JOIN organizations_users as ou ON ou.user_id = u.user_id
                JOIN user_role AS ur ON ur.user_id = u.user_id
                WHERE ou.organization_id = "{organization_id}" AND ur.role = "employee"
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
                    user_id=row["u.user_id"],
                    name=f'{row["u.first_name"]} {row["u.last_name"]}',
                    phone_number=row["u.phone_number"],
                )
            )
        return result

    def get_organization_name_by_phone(self, phone_number: str) -> str | None:
        def callee(session: ydb.Session):
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

    def get_parent_by_child_id(
        self, child_id: str
    ) -> tuple[UserModel | None, UserModel | None] | None:
        # todo: fix with child_parent table usage
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

        def callee_1(session: ydb.Session):
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

        def callee_2(session: ydb.Session):
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

    def link_role(self, user_id: str, role: models.Roles):
        def callee(session: ydb.Session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO user_role ({keys}) VALUES {values}
                """.format(
                    db_prefix=self._db_prefix,
                    keys="user_id, role",
                    values=f'("{user_id}", "{role}")',
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def delete_by_id(self, user_id: str) -> None:
        def callee(session: ydb.Session):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                delete
                FROM user
                WHERE user_id = "{user_id}"
                """.format(
                    db_prefix=self._db_prefix, user_id=user_id
                ),
                commit_tx=True,
            )

        self._pool.retry_operation_sync(callee)
