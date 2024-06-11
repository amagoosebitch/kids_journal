from models.entity import AgeRanges
from models.group import GroupModel
from models.organizations import OrganizationModel
import requests


class TestOrganizations:
    def test_add_organization(self):
        org1 = OrganizationModel(name='kek')
        add_response = requests.post('http://localhost:8080/organizations', data=org1.model_dump_json())
        assert add_response.status_code == 200

        get_response = requests.get(f'http://localhost:8080/organizations/{org1.organization_id}')
        assert get_response.status_code == 200
        assert get_response.json()['organization_id'] == str(org1.organization_id)

        org2 = OrganizationModel(name='kek')
        add_response = requests.post('http://localhost:8080/organizations', data=org2.model_dump_json())
        assert add_response.status_code == 200

        get_response = requests.get(f'http://localhost:8080/organizations/')
        assert get_response.status_code == 200
        ids = [row['organization_id'] for row in get_response.json()]
        assert str(org1.organization_id) in ids
        assert str(org2.organization_id) in ids

    def test_get_group_by_organization(self):
        org1 = OrganizationModel(name='kek')
        add_response = requests.post('http://localhost:8080/organizations', data=org1.model_dump_json())
        assert add_response.status_code == 200

        group = GroupModel(organization_id=str(org1.organization_id), name='kek', age_range=AgeRanges.ZERO_THREE)
        add_response = requests.post('http://localhost:8080/groups', data=group.model_dump_json())
        assert add_response.status_code == 200

        group_kek = GroupModel(group_id='21930129301290', organization_id='49211094', name='kek', age_range=AgeRanges.ZERO_THREE)
        add_response = requests.post('http://localhost:8080/groups', data=group_kek.model_dump_json())
        assert add_response.status_code == 200

        get_response = requests.get(f"http://localhost:8080/organizations/{org1.organization_id}/groups")
        assert get_response.status_code == 200
        assert get_response.json()[0]['group_id'] == str(group.group_id)
