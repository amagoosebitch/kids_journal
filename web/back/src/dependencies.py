from functools import cache
from typing import Annotated, Any

import ydb
from fastapi import Depends

from auth.settings import JWTSettings
from db.services.child import ChildService
from db.services.employee import EmployeeService
from db.services.groups import GroupService
from db.services.organization import OrganizationService
from db.services.parent import ParentService
from db.settings import YDBSettings


@cache
def ydb_settings() -> YDBSettings:
    return YDBSettings()


@cache
def jwt_settings() -> JWTSettings:
    return JWTSettings()


@cache
def create_pool(settings: Annotated[YDBSettings, Depends(ydb_settings)]):
    driver = ydb.Driver(
        endpoint=settings.endpoint,
        database=settings.database,
        credentials=ydb.credentials_from_env_variables(),
    )

    return ydb.SessionPool(driver)


@cache
def create_organization_service(
    pool: Annotated[Any, Depends(create_pool)],
    settings: Annotated[YDBSettings, Depends(ydb_settings)],
) -> OrganizationService:
    return OrganizationService(pool, settings.database)


@cache
def create_group_service(
    pool: Annotated[Any, Depends(create_pool)],
    settings: Annotated[YDBSettings, Depends(ydb_settings)],
) -> GroupService:
    return GroupService(pool, settings.database)


@cache
def create_parent_service(
    pool: Annotated[Any, Depends(create_pool)],
    settings: Annotated[YDBSettings, Depends(ydb_settings)],
) -> ParentService:
    return ParentService(pool, settings.database)


@cache
def create_employee_service(
    pool: Annotated[Any, Depends(create_pool)],
    settings: Annotated[YDBSettings, Depends(ydb_settings)],
) -> EmployeeService:
    return EmployeeService(pool, settings.database)


@cache
def create_child_service(
    pool: Annotated[Any, Depends(create_pool)],
    settings: Annotated[YDBSettings, Depends(ydb_settings)],
) -> ChildService:
    return ChildService(pool, settings.database)
