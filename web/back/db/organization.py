import ydb


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
                '/local'
            ),
            commit_tx=True,
        )
        for row in res[0].rows:
            print(row)

    return pool.retry_operation_sync(callee)


if __name__ == "__main__":
    with ydb.Driver(
            endpoint="grpc://localhost:2136",
            database="/local",
            credentials=ydb.credentials_from_env_variables()
    ) as driver:
        driver.wait(timeout=5, fail_fast=True)
        with ydb.SessionPool(driver) as pool:
            insert_test(pool)
            select_test(pool)
