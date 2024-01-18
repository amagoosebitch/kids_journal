from typing import Any

from db.utils import _format_unix_time
from models.child import ChildModelResponse
from models.groups import GroupModel
from models.parents import ParentModelResponse


class GroupService:
    def __init__(self, ydb_pool: Any, db_prefix: str):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def create_group(self, args_model: GroupModel):
        args = args_model.model_dump(exclude_none=False, mode="json")

        def callee(session: Any):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO group ({keys}) VALUES
                    (
                        "{group_id}",
                        "{organization_id}",
                        "{name}",
                        "{age_range}"
                    );
                """.format(
                    db_prefix=self._db_prefix,
                    keys=", ".join(args.keys()),
                    **args,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_all(self) -> list[GroupModel]:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM group
                """.format(
                    db_prefix=self._db_prefix
                ),
                commit_tx=True,
            )

        results = self._pool.retry_operation_sync(callee)[0].rows
        return [GroupModel.model_validate(result) for result in results]

    def get_all_for_organization(self, organization_id: str) -> list[GroupModel]:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM group
                WHERE organization_id = "{organization_id}"
                """.format(
                    db_prefix=self._db_prefix, organization_id=organization_id
                ),
                commit_tx=True,
            )

        results = self._pool.retry_operation_sync(callee)[0].rows
        return [GroupModel.model_validate(result) for result in results]

    def get_by_id(self, group_id: str) -> GroupModel | None:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM group
                WHERE group_id = "{group_id}"
                """.format(
                    db_prefix=self._db_prefix, group_id=group_id
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        if not rows:
            return None
        return GroupModel.model_validate(rows[0])

    def get_children_by_group_id(self, group_id: str) -> list[ChildModelResponse]:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT c.child_id, c.first_name, c.name, c.birth_date, p1.parent_id, p1.name, p1.phone_number, p2.parent_id, p2.name, p2.phone_number
                FROM child as c
                JOIN group_child on c.child_id = group_child.child_id
                JOIN parent as p1 on p1.parent_id = c.parent_1_id 
                JOIN parent as p2 on p2.parent_id = c.parent_2_id 
                WHERE group_id = "{group_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    group_id=group_id,
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        if not rows:
            return []
        result = []
        for row in rows:
            parent1 = None
            parent2 = None
            if row["p1.parent_id"] is not None:
                parent1 = ParentModelResponse(
                    parent_id=row["p1.parent_id"],
                    name=row["p1.name"],
                    phone_number=row["p1.phone_number"],
                )
            if row["p2.parent_id"] is not None:
                parent2 = ParentModelResponse(
                    parent_id=row["p2.parent_id"],
                    name=row["p2.name"],
                    phone_number=row["p2.phone_number"],
                )
            result.append(
                ChildModelResponse(
                    child_id=row["c.child_id"],
                    name=row["c.name"],
                    birth_date=_format_unix_time(row["c.birth_date"]),
                    parent_1=parent1,
                    parent_2=parent2,
                )
            )

        return result
