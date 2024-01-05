from functools import cache

from pydantic_settings import BaseSettings


class ApiClientSettings(BaseSettings):
    pass


@cache
def get_api_settings():
    pass
