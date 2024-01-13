from typing import Any
from uuid import UUID

from db.utils import _format_unix_time
from models import GroupChildModel, GroupModel
from models.child import ChildModel


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
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM group
                """.format(
                    db_prefix=self._db_prefix
                ),
                commit_tx=True,
            )

        results = self._pool.retry_operation_sync(callee)
        return [GroupModel.model_validate(result) for result in results]

    def get_all_for_organization(self, organization_id: UUID) -> list[GroupModel]:
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

    def get_by_id(self, group_id: UUID) -> GroupModel | None:
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

    def link_to_children(self, group_child_model: GroupChildModel) -> None:
        values = ", ".join(
            f'("{group_child_model.group_id}", "{child_id}")'
            for child_id in group_child_model.child_ids
        )

        def callee(session: Any):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO group_child {keys} VALUES {values}
                """.format(
                    db_prefix=self._db_prefix,
                    keys="(group_id, child_id)",
                    values=values,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_children_by_group_id(self, group_id: UUID) -> list[ChildModel]:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM child
                JOIN group_child on child.child_id = group_child.child_id
                WHERE group_id = "{group_id}"
                """.format(
                    db_prefix=self._db_prefix,
                    group_id=group_id,
                ),
                commit_tx=True,
            )

        rows = self._pool.retry_operation_sync(callee)[0].rows
        if rows is None:
            return []

        response = []
        for row in rows:
            row["start_education_date"] = _format_unix_time(row["start_education_date"])
            row["start_education_time"] = _format_unix_time(row["start_education_time"])
            row["end_education_time"] = _format_unix_time(row["end_education_time"])
            row["birth_date"] = _format_unix_time(row["birth_date"])
            response.append(ChildModel.model_validate(row))
        return response
