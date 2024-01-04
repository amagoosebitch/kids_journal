from typing import Any
from uuid import UUID

from db.models.groups import GroupModel


class GroupService:
    def __init__(self, ydb_pool: Any, db_prefix: str):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def create_group(self, args_model: GroupModel):
        args = args_model.model_dump(exclude_none=True, mode='json')

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
        return [
            GroupModel.model_validate(result) for result in results
        ]  # мейби model_validate_json если возвращает строку

    def get_all_for_organization(self, organization_id: UUID) -> list[GroupModel]:
        def callee(session: Any):
            session.transaction().execute(
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

        results = self._pool.retry_operation_sync(callee)
        return [
            GroupModel.model_validate(result) for result in results
        ]  # мейби model_validate_json если возвращает строку

    def get_by_id(self, group_id: UUID) -> GroupModel:
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

        response = self._pool.retry_operation_sync(callee)[0].rows[0]
        return GroupModel.model_validate(response)

    def get_id_by_name(self, name: str) -> UUID:
        def callee(session: Any):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT group_id
                FROM group
                WHERE name = "{name}"
                """.format(
                    db_prefix=self._db_prefix, name=name
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)
