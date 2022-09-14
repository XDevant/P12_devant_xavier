import pytest
from pytest_logic.fake_logs import user_logs

data = {
        "contact_email": "bi@bi.co",
        "client_id":  1,
        "contract_id":  1,
        "attendees":  15,
        "event_date":  "2022-08-17",
        "notes": "bla"
        }


@pytest.mark.django_db
class TestEventCreation:
    def test_sales_1_create_event(self, api_client):
        username, password = user_logs[0]
        api_client.login(username=username, password=password)
        data["client_id"] = 1
        data["contract_id"] = 1
        response = api_client.post('http://127.0.0.1:8000/events/', data=data)
        assert response.status_code == 201

    @pytest.mark.parametrize("user", [pytest.param(user_logs[i]) for i in range(0, 6)])
    def test_unauthorized_do_not_create_event(self, api_client, user):
        username, password = user
        api_client.login(username=username, password=password)
        data["client_id"] = 1
        data["contract_id"] = 2
        response = api_client.post('http://127.0.0.1:8000/events/', data=data)
        assert response.status_code >= 400

    def test_sales_2_create_event(self, api_client):
        username, password = user_logs[1]
        api_client.login(username=username, password=password)
        data["client_id"] = 2
        data["contract_id"] = 2
        response = api_client.post('http://127.0.0.1:8000/events/', data=data)
        assert response.status_code == 201
