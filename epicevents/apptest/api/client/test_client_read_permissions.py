import pytest
from copy import deepcopy
from utils.prettyprints import PrettifyGetReport, PRR
from apptest.forms import expected_client_1


@pytest.fixture
def expected():
    expected_dict = deepcopy(expected_client_1)
    expected_dict["date_updated"] = None
    return expected_dict


@pytest.mark.django_db
class TestClientRead:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2", "support_1", "support_2", "admin_1"])
    def test_contact_see_clients(self, api_client, logins, user, expected):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/clients/')
        if user == "sales_1":
            request_dict = {'url': '/clients/',
                            'logs': getattr(logins, user)}
            report = PrettifyGetReport(request_dict, response.data, expected)
            PRR.save_report(report.report, "list", model="clients", mode='w')
            assert "0 key error" in report.report[-1]
            assert "0 value error" in report.report[-1]
        assert response.status_code == 200
        assert len(response.data) > 0

    def test_unauthorized_do_not_see_clients(self, api_client, logins):
        api_client.login(**logins.visitor_1)
        response = api_client.get('/clients/')
        assert response.status_code == 403

    @pytest.mark.parametrize("user", ["sales_1", "support_1", "admin_1"])
    def test_contact_see_client_1(self, api_client, logins, user, expected):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/clients/1/')
        if user == "sales_1":
            request_dict = {'url': '/clients/1/',
                            'logs': getattr(logins, user)}
            report = PrettifyGetReport(request_dict, response.data, expected)
            PRR.save_report(report.report, "detail", model="clients", mode='w')
            assert "0 key error" in report.report[-1]
            assert "0 value error" in report.report[-1]
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
    def test_non_contact_do_not_see_client_1(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/clients/2/')
        assert response.status_code in [403, 404]




