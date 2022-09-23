import pytest


@pytest.mark.django_db
class TestClientUpdate:
    def test_contact_update_client(self, api_client, logins):
        api_client.login(**logins.sales_1)
        response = api_client.get('/clients/')
        data = response.data[0]
        assert '0123456789' not in data["phone"]
        data["phone"] = "0123456789"
        response = api_client.put('/clients/1/', data=data)
        assert response.status_code == 200
        assert '0123456789' in response.data["phone"]

    @pytest.mark.parametrize("user", ["sales_2", "support_1", "support_2", "visitor_1"])
    def test_unauthorized_do_not_update_clients(self, api_client, logins, user):
        api_client.login(**logins.sales_1)
        response = api_client.get('/clients/')
        data = response.data[0]
        data["phone"] = "0123456789"
        api_client.logout()
        api_client.login(**getattr(logins, user))
        response = api_client.put('/clients/1/', data=data)
        assert response.status_code in [403, 404]
