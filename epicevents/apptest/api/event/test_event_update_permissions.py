import pytest
from copy import deepcopy
from utils.prettyprints import Report


@pytest.mark.django_db
class TestEventUpdate:
    @pytest.mark.parametrize("user", ["support_1", "support_2", "admin_1"])
    def test_contact_update_event(self, api_client, logins, user):
        logs = getattr(logins, user)
        api_client.login(**logs)
        url = f"/events/{int(user.split('_')[-1])}/"
        response = api_client.get("/events/")
        data = response.data[0]
        assert f"test event {int(user.split('_')[-1])}" == data["notes"]
        expected = deepcopy(data)
        data["notes"] = "changing notes"
        data["contact_email"] = data["contact_email"].split(':')[-1]
        response = api_client.put(url, data=data)
        print("\n Trying to change first listed event's notes: ", end='')
        assert response.status_code == 200
        if user == "support_1":
            report = Report(url=url,
                            logs=logs,
                            action="change",
                            request_body=data,
                            expected=expected,
                            response_body=response.data)
            report.save(model="events", mode='w')
            print("Comparing updated event with expected result: ", end='')
            assert "0 key error" in report.errors
            assert "0 value error" in report.errors
        assert response.data["notes"] == 'changing notes'

    @pytest.mark.parametrize("user",
                             ["sales_1", "sales_2", "support_2", "visitor_1"])
    def test_unauthorized_cant_update_events(self, api_client, logins, user):
        api_client.login(**logins.admin_1)
        response = api_client.get('/events/')
        data = response.data[0]
        assert data["notes"] == "test event 1"
        data["contact_email"] = data["contact_email"].split("couriel:")[-1]
        api_client.login(**getattr(logins, user))
        url = f"/events/{int(user.split('_')[-1])}/"
        response = api_client.put(url, data=data)
        assert response.status_code >= 400

    @pytest.mark.parametrize("key, value",
                             [pytest.param("contact_email", "bo@bo.co"),
                              pytest.param("client_id", 2)])
    def test_support_do_not_corrupt_events(self,
                                           api_client,
                                           logins,
                                           key,
                                           value):
        api_client.login(**logins.support_1)
        response = api_client.get('/events/')
        data = response.data[0]
        assert 'test event 1' == data["notes"]
        data["contact_email"] = data["contact_email"].split("couriel:")[-1]
        data[key] = value
        response = api_client.put('/events/1/', data=data)
        assert response.status_code >= 400
