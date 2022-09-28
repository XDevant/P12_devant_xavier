import pytest


@pytest.mark.django_db
class TestClientRead:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2", "support_1", "support_2", "admin_1"])
    def test_contact_see_clients(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/clients/')
        assert response.status_code == 200
        assert len(response.data) > 0

    def test_unauthorized_do_not_see_clients(self, api_client, logins):
        api_client.login(**logins.visitor_1)
        response = api_client.get('/clients/')
        assert response.status_code == 403

    @pytest.mark.parametrize("user", ["sales_1", "support_1", "admin_1"])
    def test_contact_see_client_1(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/clients/1/')
        assert response.status_code == 200
        assert len(response.data) == 10

    @pytest.mark.parametrize("user", ["sales_2", "support_2", "visitor_1"])
    def test_non_contact_do_not_see_client_1(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/clients/1/')
        assert response.status_code in [403, 404]

    @pytest.mark.parametrize("user", ["sales_2", "support_2", "admin_1"])
    def test_contact_see_client_2(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/clients/2/')
        assert response.status_code == 200
        assert len(response.data) == 10

    @pytest.mark.parametrize("user", ["sales_1", "support_1", "visitor_1"])
    def test_non_contact_do_not_see_client_1(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/clients/2/')
        assert response.status_code in [403, 404]




