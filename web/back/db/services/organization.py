from typing import Any
from uuid import UUID

import ydb
from pydantic import ValidationError

from db.utils import _format_time, _format_unix_time
from models.organizations import OrganizationModel


def insert_test(pool: Any):
    def callee(session: Any):
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


def select_test(pool: Any):
    def callee(session: Any):
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


class OrganizationService:
    def __init__(self, ydb_pool, db_prefix):
        self._pool = ydb_pool
        self._db_prefix = db_prefix

    def create_organization(self, args_model: OrganizationModel):
        args_model.start_education_time = args_model.start_education_time.replace(
            microsecond=0
        )
        args_model.end_education_time = args_model.end_education_time.replace(
            microsecond=0
        )
        args_model.registration_date = args_model.registration_date.replace(
            microsecond=0
        )
        args_model.updated_date = args_model.updated_date.replace(microsecond=0)
        args = args_model.model_dump(exclude_none=False, mode="json")
        args["start_education_time"] = _format_time(args["start_education_time"])
        args["end_education_time"] = _format_time(args["end_education_time"])
        args["registration_date"] = _format_time(args["registration_date"])
        args["updated_date"] = _format_time(args["updated_date"])

        def callee(session: Any):
            session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                UPSERT INTO organization ({keys}) VALUES
                    (
                        "{organization_id}",
                        "{name}",
                        "{description}",
                        "{photo_url}",
                        Datetime("{start_education_time}"),
                        Datetime("{end_education_time}"),
                        Datetime("{registration_date}"),
                        Datetime("{updated_date}")
                    );
                """.format(
                    db_prefix=self._db_prefix,
                    keys=", ".join(args.keys()),
                    **args,
                ),
                commit_tx=True,
            )

        return self._pool.retry_operation_sync(callee)

    def get_all(self) -> list[OrganizationModel]:
        def callee(session: Any):
            return session.transaction().execute(
                """
                PRAGMA TablePathPrefix("{db_prefix}");
                SELECT *
                FROM organization
                """.format(
                    db_prefix=self._db_prefix
                ),
                commit_tx=True,
            )

        results = self._pool.retry_operation_sync(callee)[0]
        response: list[OrganizationModel] = []
        for row in results.rows:
            row["start_education_time"] = _format_unix_time(row["start_education_time"])
            row["end_education_time"] = _format_unix_time(row["end_education_time"])
            row["registration_date"] = _format_unix_time(row["registration_date"])
            row["updated_date"] = _format_unix_time(row["updated_date"])
            try:
                response.append(OrganizationModel.model_validate(row))
            except ValidationError:
                #  ToDo: Мега пепега опасное место
                continue
        return response

    def get_by_name(self, name: str) -> OrganizationModel:
        def callee(session: Any):
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
        def callee(session: Any):
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
        def callee(session: Any):
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
