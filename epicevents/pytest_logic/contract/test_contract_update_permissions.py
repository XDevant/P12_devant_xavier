import pytest
from pytest_logic.fake_logs import user_logs


@pytest.mark.django_db
class TestContractUpdate:
    def test_contact_update_contract(self, api_client):
        username, password = user_logs[0]
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/contracts/')
        data = response.data[0]
        assert data["amount"] == 10
        data["amount"] = 15
        response = api_client.put('http://127.0.0.1:8000/contracts/1/', data=data)
        assert response.status_code == 200
        assert response.data["amount"] == 15

    @pytest.mark.parametrize("user", [pytest.param(user_logs[i]) for i in range(1, 4)])
    def test_unauthorized_do_not_update_contracts(self, api_client, user):
        username, password = user_logs[0]
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/contracts/')
        data = response.data[0]
        assert data["amount"] == 10
        data["amount"] = 15
        username, password = user
        api_client.login(username=username, password=password)
        response = api_client.put('http://127.0.0.1:8000/contracts/1/', data=data)
        assert response.status_code in [403, 404]
