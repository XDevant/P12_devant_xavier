import pytest

data = {
                "client_id":  1,
                "status":  "False",
                "amount":  15,
                "payment_due":  "2022-08-17"
        }


@pytest.mark.django_db
class TestContractCreation:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2"])
    def test_sales_create_contract(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        data["client_id"] = int(user.split('_')[-1])
        response = api_client.post('/contracts/', data=data)
        assert response.status_code == 201

    @pytest.mark.parametrize("user", ["support_1", "support_2", "admin_1", "visitor_1"])
    def test_unauthorized_do_not_create_contract(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        data["client_id"] = 1
        response = api_client.post('/contracts/', data=data)
        assert response.status_code >= 400

    @pytest.mark.parametrize("user", ["sales_1", "sales_2"])
    def test_sales_do_not_create_contract_for_wrong_client(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        data["client_id"] = int(user.split('_')[-1]) % 2 + 1
        response = api_client.post('/contracts/', data=data)
        assert response.status_code == 400
