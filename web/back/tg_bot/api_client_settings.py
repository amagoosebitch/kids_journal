from functools import cache

from pydantic_settings import BaseSettings
from yarl import URL


class ApiClientSettings(BaseSettings):
    url: URL = URL("http://127.0.0.1:8000")
    employee_endpoint: str = "employee/{tgId}"
    parent_endpoint: str = "parents/{tgId}"

    @property
    def employee_url(self) -> URL:
        return self.url / self.employee_endpoint

    @property
    def parent_url(self) -> URL:
        return self.url / self.parent_endpoint

    class Config:
        env_prefix = "API_"


@cache
def get_api_settings() -> ApiClientSettings:
    return ApiClientSettings()
