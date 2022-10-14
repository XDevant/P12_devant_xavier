import pytest
from copy import deepcopy
from utils.prettyprints import Report
from apptest.forms import expected_client_1


@pytest.fixture
def expected():
    expected_dict = deepcopy(expected_client_1)
    expected_dict["date_updated"] = None
    return expected_dict


@pytest.mark.django_db
class TestClientRead:
    @pytest.mark.parametrize("user", ["sales_1",
                                      "sales_2",
                                      "support_1",
                                      "support_2",
                                      "admin_1"])
    def test_contact_see_clients(self, api_client, logins, user, expected):
        url = '/clients/'
        logs = getattr(logins, user)
        api_client.login(**logs)
        response = api_client.get(url)
        if user == "sales_1":
            report = Report(url=url,
                            logs=logs,
                            action="list",
                            response_body=response.data)
            report.save(model="clients", mode='w')
            report = Report(url=url,
                            logs=logs,
                            action="list",
                            expected=expected,
                            response_body=response.data)
            assert "0 key error" in report.errors
            assert "0 value error" in report.errors
        assert response.status_code == 200
        if user != "admin_1":
            assert len(response.data) == 2
        else:
            assert len(response.data) == 4

    def test_unauthorized_do_not_see_clients(self, api_client, logins):
        api_client.login(**logins.visitor_1)
        response = api_client.get('/clients/')
        assert response.status_code == 403

    @pytest.mark.parametrize("user", ["sales_1", "support_1", "admin_1"])
    def test_contact_see_client_1(self, api_client, logins, user, expected):
        url = '/clients/1/'
        logs = getattr(logins, user)
        api_client.login(**logs)
        response = api_client.get(url)
        if user == "sales_1":
            report = Report(url=url,
                            logs=logs,
                            action="detail",
                            expected=expected,
                            response_body=response.data)
            report.save(model="clients", mode='w')
            assert "0 key error" in report.errors
            assert "0 value error" in report.errors
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
    def test_non_contact_do_not_see_client_2(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/clients/2/')
        assert response.status_code in [403, 404]
