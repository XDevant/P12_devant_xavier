import pytest
from pytest_logic.fake_logs import user_logs


@pytest.mark.django_db
class TestClientUpdate:
    def test_contact_update_client(self, api_client):
        username, password = user_logs[0]
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/clients/')
        data = response.data[0]
        assert '0123456789' not in data["phone"]
        data["phone"] = "0123456789"
        response = api_client.put('http://127.0.0.1:8000/clients/1/', data=data)
        assert response.status_code == 200
        assert '0123456789' in response.data["phone"]

    @pytest.mark.parametrize("user", [pytest.param(user_logs[i]) for i in [1, 2, 3]])
    def test_unauthorized_do_not_update_clients(self, api_client, user):
        username, password = user
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/clients/')
        data = response.data[0]
        data["phone"] = "0123456789"
        response = api_client.put('http://127.0.0.1:8000/clients/1/', data=data)
        assert response.status_code in [403, 404]
