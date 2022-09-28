import pytest
from apptest.forms import event_form as data


@pytest.mark.django_db
class TestEventCreation:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2"])
    def test_sales_create_event(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        data["client_id"] = int(user.split('_')[-1])
        data["contract_id"] = int(user.split('_')[-1])
        response = api_client.post('/events/', data=data)
        assert response.status_code == 201

    @pytest.mark.parametrize("user", ["sales_2", "support_1", "support_2", "admin_1", "visitor_1"])
    def test_unauthorized_do_not_create_event(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        data["client_id"] = 1
        data["contract_id"] = 1
        response = api_client.post('/events/', data=data)
        assert response.status_code >= 400

    @pytest.mark.parametrize("user", ["sales_1", "sales_2"])
    def test_sales_can_not_create_impossible_event(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        data["client_id"] = 1
        data["contract_id"] = 2
        response = api_client.post('/events/', data=data)
        assert response.status_code >= 400
