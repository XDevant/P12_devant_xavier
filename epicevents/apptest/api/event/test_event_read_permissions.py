import pytest
from copy import deepcopy
from utils.prettyprints import Report
from apptest.forms import expected_event_1


@pytest.fixture
def expected():
    expected_dict = deepcopy(expected_event_1)
    expected_dict["date_updated"] = None
    return expected_dict


@pytest.mark.django_db
class TestEventRead:
    @pytest.mark.parametrize(
        "user", ["sales_1", "sales_2", "support_1", "support_2", "admin_1"])
    def test_contact_see_events(self, api_client, logins, user, expected):
        url = '/events/'
        logs = getattr(logins, user)
        api_client.login(**logs)
        response = api_client.get(url)
        assert response.status_code == 200
        if user == "sales_1":
            report = Report(url=url,
                            logs=logs,
                            action="list",
                            response_body=response.data)
            report.save(model="events", mode='w')
            report = Report(url=url,
                            logs=logs,
                            action="list",
                            expected=expected,
                            response_body=response.data)
            assert "0 key error" in report.errors
            assert "0 value error" in report.errors
        if user != "admin_1":
            assert len(response.data) == 2
        else:
            assert len(response.data) == 4

    @pytest.mark.parametrize("user", ["visitor_1"])
    def test_unauthorized_do_not_see_events(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/events/')
        assert response.status_code == 403

    @pytest.mark.parametrize(
        "user", ["sales_1", "sales_2", "support_1", "support_2", "admin_1"])
    def test_contact_i_see_event_i(self, api_client, logins, user, expected):
        url = f"/events/{int(user.split('_')[-1])}/"
        logs = getattr(logins, user)
        api_client.login(**logs)
        response = api_client.get(url)
        assert response.status_code == 200
        if user == "sales_1":
            report = Report(url=url,
                            logs=logs,
                            action="detail",
                            expected=expected,
                            response_body=response.data)
            report.save(model="events", mode='w')
            assert "0 key error" in report.errors
            assert "0 value error" in report.errors
        assert len(response.data) == 9

    @pytest.mark.parametrize(
        "user", ["sales_1", "sales_2", "support_1", "support_2"])
    def test__contact_i_do_not_see_event_j(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        url = f"/events/{int(user.split('_')[-1]) % 2 + 1}/"
        response = api_client.get(url)
        assert response.status_code in [403, 404]
