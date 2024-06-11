from functools import cache

from pydantic_settings import BaseSettings
from yarl import URL


class ApiClientSettings(BaseSettings):
    url: str = "http://127.0.0.1:8080"
    employee_endpoint: str = "employee/{tg_id}"
    user_endpoint: str = "user_merge"
    parent_endpoint: str = "parents/{tg_id}"
    parents_by_child_endpoint: str = "parents/child/{child_id}"
    group_endpoint: str = "groups/{group_id}"
    children_by_group_endpoint: str = "{group_id}/child"
    organization_by_phone: str = "employee/{phone}/organizations"
    groups_by_organization: str = "organizations/{organization_id}/groups"

    def get_parents_by_child_url(self, child_id: str) -> URL:
        return URL(self.url) / self.parents_by_child_endpoint.format(child_id=child_id)

    def get_children_by_group_url(self, group_id: str) -> URL:
        return URL(self.url) / self.children_by_group_endpoint.format(group_id=group_id)

    def get_employee_url(self, tg_id: int) -> URL:
        return URL(self.url) / self.employee_endpoint.format(tg_id=tg_id)

    def get_user_url(self) -> URL:
        return URL(self.url) / self.user_endpoint

    def get_parent_url(self, tg_id: int) -> URL:
        return URL(self.url) / self.parent_endpoint.format(tg_id=tg_id)

    def get_group_url(self, group_id: str) -> URL:
        return URL(self.url) / self.group_endpoint.format(group_id=group_id)

    def get_organization_by_phone_url(self, phone: str) -> URL:
        return URL(self.url) / self.organization_by_phone.format(phone=phone)

    def get_groups_by_organization_url(self, organization: str) -> URL:
        return URL(self.url) / self.groups_by_organization.format(
            organization_id=organization
        )

    class Config:
        env_prefix = "API_CLIENT_"


@cache
def get_api_settings() -> ApiClientSettings:
    return ApiClientSettings()
