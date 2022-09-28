import pytest


@pytest.mark.django_db
class TestContractUpdate:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2", "admin_1"])
    def test_contact_update_contract(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/contracts/')
        data = response.data[0]
        assert data["amount"] != 156331
        data["sales_contact"] = data["contact"].split("couriel:")[-1]
        data["amount"] = 156331
        response = api_client.put(f"/contracts/{int(user.split('_')[-1])}/", data=data)
        print(f"\n Trying to change first listed contract's amount: ", end='')
        assert response.status_code == 200
        assert response.data["amount"] == 156331

    @pytest.mark.parametrize("user", ["sales_2", "support_1", "support_2", "visitor_1"])
    def test_unauthorized_do_not_update_contracts(self, api_client, logins, user):
        api_client.login(**logins.admin_1)
        response = api_client.get('/contracts/')
        data = response.data[0]
        assert data["amount"] != 156331
        data["amount"] = 156331
        api_client.logout()
        api_client.login(**getattr(logins, user))
        response = api_client.put('/contracts/1/', data=data)
        print(f"\n Trying to change first listed contract's amount: ", end='')
        assert response.status_code in [403, 404]
