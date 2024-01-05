import requests
from cachetools.func import ttl_cache

from tg_bot.api_client_settings import get_api_settings

api_settings = get_api_settings()


@ttl_cache(ttl=3600)
def get_employee_by_tg_id(tg_id: int) -> dict:
    return requests.get(
        api_settings.employee_url,
        params={"tg_id": tg_id},
    ).json()


@ttl_cache(ttl=3600)
def get_parent_by_tg_id(tg_id: int) -> dict:
    return requests.get(
        api_settings.parent_url,
        params={"tg_id": tg_id},
    ).json()


@ttl_cache(ttl=3600)
def get_group_by_id(group_id: str) -> dict:
    return requests.get(
        api_settings.parent_url,
        params={"group_id": group_id},
    ).json()
