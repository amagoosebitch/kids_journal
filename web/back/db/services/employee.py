import json
from typing import Any

from db.models.employees import EmployeeModel


class EmployeeService:
    def __init__(self, ydb_pool: Any, db_prefix: str):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def create_employee(self, args_model: EmployeeModel) -> None:
        args = args_model.model_dump(exclude_none=False, mode="json")

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
        return EmployeeModel.model_validate(rows[0])
