import requests

from models.child import ChildModel
from models.employees import EmployeeModel
from models.groups import GroupModel
from models.parents import ParentModel
from tg_bot.api_client_settings import get_api_settings

api_settings = get_api_settings()


def get_employee_by_tg_id(tg_id: int) -> EmployeeModel | None:
    response = requests.get(
        api_settings.get_employee_url(tg_id=tg_id),
    ).json()
    if response is None:
        return response
    return EmployeeModel.model_validate(response)


def get_children_by_group_id(group_id: str) -> list[ChildModel]:
    response = requests.get(
        api_settings.get_children_by_group_url(group_id=group_id),
    )
    print(response)
    response = response.json()
    return [ChildModel.model_validate(row) for row in response]


def get_parent_by_tg_id(tg_id: int) -> ParentModel | None:
    response = requests.get(
        api_settings.get_parent_url(tg_id=tg_id),
    ).json()
    if response is None:
        return response
    return ParentModel.model_validate(response)


def get_parents_by_child_id(child_id: str) -> tuple[ParentModel, ParentModel] | None:
    response = requests.get(
        api_settings.get_parents_by_child_url.format(child_id=child_id)
    ).json()
    if response is None:
        return response
    return ParentModel.model_validate(response[0]), ParentModel.model_validate(
        response[1]
    )


def get_group_by_id(group_id: str) -> GroupModel | None:
    response = requests.get(
        api_settings.get_group_url(group_id=group_id),
    ).json()
    if response is None:
        return response
    return GroupModel.model_validate(response)


def try_merge_user_by_phone(
    phone: str, tg_id: int
) -> ParentModel | EmployeeModel | None:
    response = requests.post(
        api_settings.get_user_url(),
        json={"phone_number": phone, "tg_user_id": str(tg_id)},
    ).json()
    if response is None:
        return None

    if response["role"] == "parent":
        return ParentModel.model_validate(response["data"])
    elif response["role"] == "employee":
        return EmployeeModel.model_validate(response["data"])
    return None
