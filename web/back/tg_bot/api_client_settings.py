from functools import cache

from pydantic_settings import BaseSettings
from yarl import URL


class ApiClientSettings(BaseSettings):
    url: str = "http://127.0.0.1:8000"
    employee_endpoint: str = "employee/{tgId}"
    user_endpoint: str = "user_merge"
    parent_endpoint: str = "parents/{tgId}"
    parents_by_child_endpoint: str = "parents/child/{childId}"
    group_endpoint: str = "groups/{groupId}"
    children_by_group_endpoint: str = "child/{groupId}"

    @property
    def parents_by_child_url(self) -> URL:
        return URL(self.url) / self.parents_by_child_endpoint

    @property
    def children_by_group_url(self) -> URL:
        return URL(self.url) / self.children_by_group_endpoint

    @property
    def employee_url(self) -> URL:
        return URL(self.url) / self.employee_endpoint

    @property
    def user_url(self) -> URL:
        return URL(self.url) / self.user_endpoint

    @property
    def parent_url(self) -> URL:
        return URL(self.url) / self.parent_endpoint

    @property
    def group_url(self) -> URL:
        return URL(self.url) / self.group_endpoint

    class Config:
        env_prefix = "API_CLIENT_"


@cache
def get_api_settings() -> ApiClientSettings:
    return ApiClientSettings()
