from uuid import UUID, uuid4

from pydantic import BaseModel

from db.entity import AgeRanges


class GroupModel(BaseModel):
    group_id: UUID = uuid4()
    organization_id: UUID = uuid4()
    name: str
    age_range: AgeRanges


class GroupService:
    def __init__(self, ydb_pool, db_prefix):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def create_group(self, args_model: GroupModel):
        args = args_model.model_dump(exclude_none=True)

        def callee(session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO group ({keys}) VALUES
                    ({values});
                """.format(
                    db_prefix=self._db_prefix,
                    keys=", ".join(args.keys()),
                    values=", ".join(args.values()),
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_all(self) -> list[GroupModel]:
        def callee(session):
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
        def callee(session):
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
        def callee(session):
            session.transaction().execute(
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

        return self._pool.retry_operation_sync(callee)

    def get_id_by_name(self, name: str) -> UUID:
        def callee(session):
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
