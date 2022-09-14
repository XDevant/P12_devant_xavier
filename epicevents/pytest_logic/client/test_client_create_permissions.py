import pytest
from pytest_logic.fake_logs import user_logs

data = {
                "first_name":  "third",
                "last_name":  "client",
                "email":  "third@client.co",
                "phone":  "01",
                "mobile":  "08",
                "company_name":  "World"
        }


@pytest.mark.django_db
class TestClientCreation:
    @pytest.mark.parametrize("user", [pytest.param(user_logs[i]) for i in [0, 1]])
    def test_sales_create_client(self, api_client, user):
        username, password = user
        api_client.login(username=username, password=password)
        response = api_client.post('http://127.0.0.1:8000/clients/', data=data)
        assert response.status_code == 201

    @pytest.mark.parametrize("user", [pytest.param(user_logs[i]) for i in [2, 3, 4, 5]])
    def test_unauthorized_do_not_create_client(self, api_client, user):
        username, password = user
        api_client.login(username=username, password=password)
        response = api_client.post('http://127.0.0.1:8000/clients/', data=data)
        assert response.status_code == 403
