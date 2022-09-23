import pytest


@pytest.mark.django_db
class TestContractRead:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2", "admin_1"])
    def test_sales_see_contracts(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/contracts/')
        assert response.status_code == 200

    @pytest.mark.parametrize("user", ["support_1", "support_2", "visitor_1"])
    def test_unauthorized_do_not_see_contracts(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/contracts/')
        assert response.status_code in [204, 403]

    @pytest.mark.parametrize("user", ["sales_1", "sales_2", "admin_1"])
    def test_sales_i_see_contract_i(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get(f"/contracts/{int(user.split('_')[-1])}/")
        assert response.status_code == 200

    @pytest.mark.parametrize("user", ["support_1", "support_2", "visitor_1"])
    def test_non_sales_do_not_see_contract_1(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/contracts/1/')
        assert response.status_code in [204, 403, 404]

    @pytest.mark.parametrize("user", ["sales_1", "sales_2"])
    def test_sales_non_contact_do_not_see_contract(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get(f"/contracts/{int(user.split('_')[-1]) % 2 + 1}/")
        assert response.status_code in [204, 403, 404]
