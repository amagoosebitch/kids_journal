from typing import Annotated, Any

import ydb
from fastapi import Depends

from db.services.groups import GroupService
from db.services.organization import OrganizationService
from db.settings import YDBSettings


def ydb_settings() -> YDBSettings:
    return YDBSettings()


def create_pool(settings: YDBSettings):
    driver = ydb.Driver(
        endpoint=settings.endpoint,
        database=settings.database,
        credentials=ydb.credentials_from_env_variables(),
    )

    return ydb.SessionPool(driver)


def create_organization_service(
    pool: Annotated[Any, Depends(create_pool)],
    settings: Annotated[YDBSettings, Depends(ydb_settings)],
) -> OrganizationService:
    return OrganizationService(pool, settings.database)


def create_group_service(
    pool: Annotated[Any, Depends(create_pool)],
    settings: Annotated[YDBSettings, Depends(ydb_settings)],
) -> GroupService:
    return GroupService(pool, settings.database)
