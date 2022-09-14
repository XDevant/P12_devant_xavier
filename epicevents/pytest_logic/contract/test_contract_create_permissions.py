import pytest
from pytest_logic.fake_logs import user_logs

data = {
                "client_id":  1,
                "status":  "False",
                "amount":  15,
                "payment_due":  "2022-08-17"
        }


@pytest.mark.django_db
class TestContractCreation:
    def test_sales_create_contract(self, api_client):
        username, password = user_logs[0]
        api_client.login(username=username, password=password)
        response = api_client.post('http://127.0.0.1:8000/contracts/', data=data)
        assert response.status_code == 201

    @pytest.mark.parametrize("user", [pytest.param(user_logs[i]) for i in range(1, 6)])
    def test_unauthorized_do_not_create_contract(self, api_client, user):
        username, password = user
        api_client.login(username=username, password=password)
        data["client_id"] = 1
        response = api_client.post('http://127.0.0.1:8000/contracts/', data=data)
        assert response.status_code >= 400

    def test_sales_create_contract_2(self, api_client):
        username, password = user_logs[1]
        api_client.login(username=username, password=password)
        data["client_id"] = 2
        response = api_client.post('http://127.0.0.1:8000/contracts/', data=data)
        assert response.status_code == 201
