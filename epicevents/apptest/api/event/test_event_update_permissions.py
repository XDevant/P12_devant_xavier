import pytest


@pytest.mark.django_db
class TestEventUpdate:
    @pytest.mark.parametrize("user", ["support_1", "support_2", "admin_1"])
    def test_contact_update_event(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/events/')
        data = response.data[0]
        assert f"test event {int(user.split('_')[-1])}" == data["notes"]
        data["contact_email"] = data["contact_email"].split("couriel:")[-1]
        data["notes"] = "changing notes"
        response = api_client.put(f"/events/{int(user.split('_')[-1])}/", data=data)
        assert response.status_code == 200
        assert response.data["notes"] == 'changing notes'

    @pytest.mark.parametrize("user", ["sales_1", "sales_2", "support_2", "visitor_1"])
    def test_unauthorized_do_not_update_events(self, api_client, logins, user):
        api_client.login(**logins.admin_1)
        response = api_client.get('/events/')
        data = response.data[0]
        assert data["notes"] == "test event 1"
        data["contact_email"] = data["contact_email"].split("couriel:")[-1]
        api_client.login(**getattr(logins, user))
        response = api_client.put(f"/events/{int(user.split('_')[-1])}/", data=data)
        assert response.status_code >= 400

    @pytest.mark.parametrize("key, value", [pytest.param("contact_email", "bo@bo.co"),
                                            pytest.param("client_id", 2),
                                            ])
    def test_support_do_not_update_impossible_events(self, api_client, logins, key, value):
        api_client.login(**logins.support_1)
        response = api_client.get('/events/')
        data = response.data[0]
        assert 'test event 1' == data["notes"]
        data["contact_email"] = data["contact_email"].split("couriel:")[-1]
        data[key] = value
        response = api_client.put('/events/1/', data=data)
        assert response.status_code >= 400
