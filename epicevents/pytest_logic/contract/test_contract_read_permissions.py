import pytest
from pytest_logic.fake_logs import user_logs


@pytest.mark.django_db
class TestContractRead:
    @pytest.mark.parametrize("user", [pytest.param(user_logs[i]) for i in [0, 1, 4]])
    def test_sales_see_contracts(self, api_client, user):
        username, password = user
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/contracts/')
        assert response.status_code == 200

    def test_unauthorized_do_not_see_contracts(self, api_client):
        username, password = user_logs[5]
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/contracts/')
        assert response.status_code in [204, 403]

    @pytest.mark.parametrize("user", [pytest.param(user_logs[i],) for i in [0, 4]])
    def test_contact_see_contract_1(self, api_client, user):
        username, password = user
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/contracts/1/')
        assert response.status_code == 200

    @pytest.mark.parametrize("user", [pytest.param(user_logs[i], ) for i in [1, 2, 3, 5]])
    def test_non_contact_do_not_see_contract_1(self, api_client, user):
        username, password = user
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/contracts/1/')
        assert response.status_code in [204, 403, 404]

    def test_contact_see_contract_2(self, api_client):
        username, password = user_logs[1]
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/contracts/2/')
        assert response.status_code == 200

    def test_non_contact_do_not_see_client_2(self, api_client):
        username, password = user_logs[0]
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/contracts/2/')
        assert response.status_code in [204, 403, 404]




