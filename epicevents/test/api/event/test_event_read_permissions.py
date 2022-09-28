import pytest


@pytest.mark.django_db
class TestEventRead:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2", "support_1", "support_2", "admin_1"])
    def test_contact_see_events(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/events/')
        assert response.status_code == 200

    @pytest.mark.parametrize("user", ["visitor_1"])
    def test_unauthorized_do_not_see_events(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/events/')
        assert response.status_code in [403]

    @pytest.mark.parametrize("user", ["sales_1", "sales_2", "support_1", "support_2", "admin_1"])
    def test_contact_i_see_event_i(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get(f"/events/{int(user.split('_')[-1])}/")
        assert response.status_code == 200

    @pytest.mark.parametrize("user", ["sales_1", "sales_2", "support_1", "support_2"])
    def test__contact_i_do_not_see_event_j(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get(f"/events/{int(user.split('_')[-1]) % 2 + 1}/")
        assert response.status_code in [403, 404]
