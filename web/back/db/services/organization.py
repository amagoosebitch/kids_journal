from datetime import datetime
from uuid import UUID, uuid4

import ydb
from pydantic import BaseModel


def insert_test(pool):
    def callee(session):
        session.transaction().execute(
            """
            PRAGMA TablePathPrefix("{}");
            UPSERT INTO organization (organization_id, description) VALUES
                (1, "kek");
            """.format(
                "/local"
            ),
            commit_tx=True,
        )

    return pool.retry_operation_sync(callee)


def select_test(pool):
    def callee(session):
        res = session.transaction(ydb.SerializableReadWrite()).execute(
            """
            PRAGMA TablePathPrefix("{}");
            SELECT *
            FROM organization
            """.format(
                "/local"
            ),
            commit_tx=True,
        )
        for row in res[0].rows:
            print(row)

    return pool.retry_operation_sync(callee)


class OrganizationModel(BaseModel):
    organization_id: UUID = uuid4()
    name: str
    description: str | None = None
    photo_url: str | None = None
    start_education_time: datetime
    end_education_time: datetime
    registration_date: datetime = datetime.utcnow()
    updated_date: datetime = datetime.utcnow()


class OrganizationService:
    def __init__(self, ydb_pool, db_prefix):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def create_organization(self, args_model: OrganizationModel):
        args = args_model.model_dump(exclude_none=True)

        def callee(session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO organization ({keys}) VALUES
                    ({values});
                """.format(
                    db_prefix=self._db_prefix,
                    keys=", ".join(args.keys()),
                    values=", ".join(args.values()),
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_all(self) -> list[OrganizationModel]:
        def callee(session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM organization
                """.format(
                    db_prefix=self._db_prefix
                ),
                commit_tx=True,
            )

        results = self._pool.retry_operation_sync(callee)
        return [
            OrganizationModel.model_validate(result) for result in results
        ]  # мейби model_validate_json если возвращает строку

    def get_by_name(self, name: str) -> OrganizationModel:
        def callee(session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM organization
                WHERE name = "{name}"
                """.format(
                    db_prefix=self._db_prefix, name=name
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_by_id(self, organization_id: UUID) -> OrganizationModel:
        def callee(session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM organization
                WHERE organization_id = "{organization_id}"
                """.format(
                    db_prefix=self._db_prefix, organization_id=organization_id
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_id_by_name(self, name: str) -> UUID:
        def callee(session):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT organization_id
                FROM organization
                WHERE name = "{name}"
                """.format(
                    db_prefix=self._db_prefix, name=name
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)


if __name__ == "__main__":
    with ydb.Driver(
        endpoint="grpc://localhost:2136",
        database="/local",
        credentials=ydb.credentials_from_env_variables(),
    ) as driver:
        driver.wait(timeout=5, fail_fast=True)
        with ydb.SessionPool(driver) as pool:
            insert_test(pool)
            select_test(pool)
