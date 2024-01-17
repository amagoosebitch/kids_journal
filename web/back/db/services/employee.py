import json
from typing import Any

from models.employees import EmployeeModel, EmployeeResponse
from models.role import Role


class EmployeeService:
    def __init__(self, ydb_pool: Any, db_prefix: str):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def create_employee(self, args_model: EmployeeModel) -> None:
        args = args_model.model_dump(exclude_none=False, mode="json")

        args["role_id"] = args_model.role_id.name

        def callee(session: Any):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO employee ({keys}) VALUES
                    (
                        "{employee_id}",
                        "{name}",
                        "{first_name}",
                        "{last_name}",
                        "{email}",
                        "{gender}",
                        "{phone_number}",
                        "{tg_user_id}",
                        "{role_id}",
                        "{group_ids}"
                    );
                """.format(
                    db_prefix=self._db_prefix,
                    keys=", ".join(args.keys()),
                    **args,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_by_tg_user_id(self, tg_user_id: str) -> EmployeeModel | None:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM employee
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
        rows[0]["role_id"] = Role[rows[0]["role_id"]].value
        return EmployeeModel.model_validate(rows[0])

    def get_by_phone(self, phone_number: str) -> EmployeeModel | None:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM employee
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
        rows[0]["role_id"] = Role[rows[0]["role_id"]].value
        return EmployeeModel.model_validate(rows[0])

    def set_telegram_id(self, phone_number: str, tg_user_id: str) -> bool:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPDATE employee
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

    def link_to_groups(self, group_ids: list[str], teacher_id: str):
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

    def get_by_organization_id(self, organization_id: str) -> list[EmployeeResponse]:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT DISTINCT e.employee_id, e.name, e.phone_number, e.role_id
                FROM employee as e
                JOIN group_teacher as gt ON gt.teacher_id = e.employee_id
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
            row["role_id"] = Role[row["e.role_id"]].value
            result.append(
                EmployeeResponse(
                    employee_id=row['e.employee_id'],
                    name=row['e.name'],
                    phone_number=row['e.phone_number'],
                    role_id=row['role_id'],
                )
            )
        return result

    def get_get_organization_name_by_phone(self, phone_number: str) -> str | None:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT org.name
                FROM employee as e
                JOIN group_teacher as gt ON gt.teacher_id = e.employee_id
                JOIN group as g ON g.group_id = gt.group_id
                JOIN organization as org ON org.organization_id = g.organization_id
                WHERE e.phone_number = "{phone_number}"
                """.format(
                    db_prefix=self._db_prefix,
                    phone_number=phone_number,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)[0].rows