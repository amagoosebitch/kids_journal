import requests
from cachetools.func import ttl_cache

from db.models.employees import EmployeeModel
from db.models.groups import GroupModel
from db.models.parents import ParentModel
from tg_bot.api_client_settings import get_api_settings

api_settings = get_api_settings()


@ttl_cache(ttl=3600)
def get_employee_by_tg_id(tg_id: int) -> EmployeeModel | None:
    response = requests.get(
        api_settings.employee_url,
        params={"tg_id": tg_id},
    ).json()
    if response is None:
        return response
    return EmployeeModel.model_validate(response)


@ttl_cache(ttl=3600)
def get_parent_by_tg_id(tg_id: int) -> ParentModel | None:
    response = requests.get(
        api_settings.parent_url,
        params={"tg_id": tg_id},
    ).json()
    if response is None:
        return response
    return ParentModel.model_validate(response)


@ttl_cache(ttl=3600)
def get_group_by_id(group_id: str) -> GroupModel | None:
    response = requests.get(
        api_settings.group_url,
        params={"group_id": group_id},
    ).json()
    if response is None:
        return response
    return GroupModel.model_validate(response)
