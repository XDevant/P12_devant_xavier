import pytest


@pytest.mark.django_db
class TestClientDelete:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2", "support_1", "support_2", "admin_1", "visitor_1"])
    def test_do_not_delete_client(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.delete('/clients/1/')
        assert response.status_code == 403
