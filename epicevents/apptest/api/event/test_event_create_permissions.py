import pytest
from copy import deepcopy
from apptest.forms import event_form, expected_event
from utils.prettyprints import PrettifyRequestReport


@pytest.fixture
def data():
    form = deepcopy(event_form)
    return form


@pytest.fixture
def expected():
    expected_dict = deepcopy(expected_event)
    return expected_dict


@pytest.mark.django_db
class TestEventCreation:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2"])
    def test_sales_create_event(self, api_client, logins, user, data, expected):
        api_client.login(**getattr(logins, user))
        data["status"] = int(user.split('_')[-1]) * 2
        expected["id"] = int(user.split('_')[-1]) + 2
        expected["client_id"] = int(user.split('_')[-1])
        response = api_client.post('/events/', data=data)
        print("\n")
        report = PrettifyRequestReport(data, response.data, expected, [0, 1])
        report.pretty_print()
        assert response.status_code == 201

    @pytest.mark.parametrize("user", ["sales_2", "support_1", "support_2", "admin_1", "visitor_1"])
    def test_unauthorized_do_not_create_event(self, api_client, logins, user, data):
        api_client.login(**getattr(logins, user))
        data["status"] = 2
        response = api_client.post('/events/', data=data)
        print(f"\nTrying to create event without being sales contact.", end='')
        assert response.status_code in [400, 403]

    @pytest.mark.parametrize("user", ["sales_1", "sales_2"])
    def test_contract_can_not_have_second_event(self, api_client, logins, user, data):
        api_client.login(**getattr(logins, user))
        resp_status = [1, 3]
        data["status"] = resp_status[int(user.split('_')[-1]) - 1]
        response = api_client.post('/events/', data=data)
        print(f"\nTrying to create second event for contract {data['status']}", end='')
        assert response.status_code == 400
