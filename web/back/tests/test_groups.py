import requests

from models.entity import AgeRanges
from models.group import GroupModel


class TestGroups:
    def test_add_groups(self):
        group = GroupModel(organization_id='1', name='kek', age_range=AgeRanges.ZERO_THREE)
        add_response = requests.post('http://localhost:8080/groups', data=group.model_dump_json())
        assert add_response.status_code == 200

        get_response = requests.get(f'http://localhost:8080/groups/{group.group_id}')
        assert get_response.status_code == 200
        assert get_response.text == group.model_dump_json()
