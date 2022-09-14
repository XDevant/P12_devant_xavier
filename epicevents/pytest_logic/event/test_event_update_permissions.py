import pytest
from pytest_logic.fake_logs import user_logs


@pytest.mark.django_db
class TestEventUpdate:
    def test_contact_update_event(self, api_client):
        username, password = user_logs[2]
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/events/')
        data = response.data[0]
        assert 'test event 1' == data["notes"]
        data["contact_email"] = data["contact_email"].split("couriel:")[-1]
        data["notes"] = "bla"
        response = api_client.put('http://127.0.0.1:8000/events/1/', data=data)
        assert response.status_code == 200
        assert response.data["notes"] == 'bla'

    @pytest.mark.parametrize("user", [pytest.param(user_logs[i]) for i in [0, 1, 3, 5]])
    def test_unauthorized_do_not_update_events(self, api_client, user):
        username, password = user_logs[0]
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/events/')
        data = response.data[0]
        assert data["notes"] == 'test event 1'
        data["contact_email"] = data["contact_email"].split("couriel:")[-1]
        username, password = user
        api_client.login(username=username, password=password)
        response = api_client.put('http://127.0.0.1:8000/events/1/', data=data)
        assert response.status_code >= 400

    @pytest.mark.parametrize("key, value", [pytest.param("contact_email", "bo@bo.co"),
                                            pytest.param("client_id", 2),
                                            pytest.param("contract_id", 2),
                                            ])
    def test_support_do_not_update_impossible_events(self, api_client, key, value):
        username, password = user_logs[2]
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/events/')
        data = response.data[0]
        assert 'test event 1' == data["notes"]
        data["contact_email"] = data["contact_email"].split("couriel:")[-1]
        data[key] = value
        response = api_client.put('http://127.0.0.1:8000/events/1/', data=data)
        assert response.status_code >= 400
