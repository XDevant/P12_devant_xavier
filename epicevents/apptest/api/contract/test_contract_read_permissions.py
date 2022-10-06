import pytest
from copy import deepcopy
from utils.prettyprints import PrettifyGetReport, PRR
from apptest.forms import expected_contract_1


@pytest.fixture
def expected():
    expected_dict = deepcopy(expected_contract_1)
    expected_dict["date_updated"] = None
    return expected_dict


@pytest.mark.django_db
class TestContractRead:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2", "admin_1"])
    def test_sales_see_contracts(self, api_client, logins, user, expected):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/contracts/')

        if user == "sales_1":
            request_dict = {'url': '/contracts/',
                            'logs': logins.sales_1}
            report = PrettifyGetReport(request_dict, response.data, expected)
            PRR.save_report(report.report, "list", model="contracts", mode='w')
            assert "0 key error" in report.report[-1]
            assert "0 value error" in report.report[-1]

        assert response.status_code == 200
        assert len(response.data) > 0

    @pytest.mark.parametrize("user", ["support_1", "support_2", "visitor_1"])
    def test_unauthorized_do_not_see_contracts(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/contracts/')
        assert response.status_code == 403

    @pytest.mark.parametrize("user", ["sales_1", "sales_2", "admin_1"])
    def test_sales_i_see_contract_i(self, api_client, logins, user, expected):
        api_client.login(**getattr(logins, user))
        url = f"/contracts/{int(user.split('_')[-1]) * 2 - 1}/"
        response = api_client.get(url)

        if user == "sales_1":
            request_dict = {'url': '/contracts/1/',
                            'logs': logins.sales_1}
            report = PrettifyGetReport(request_dict, response.data, expected)
            PRR.save_report(report.report, "detail", model="contracts", mode='w')
            assert "0 key error" in report.report[-1]
            assert "0 value error" in report.report[-1]

        assert response.status_code == 200
        assert len(response.data) == 8

    @pytest.mark.parametrize("user", ["support_1", "support_2", "visitor_1"])
    def test_non_sales_do_not_see_contract_1(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/contracts/1/')
        assert response.status_code in [403, 404]

    @pytest.mark.parametrize("user", ["sales_1", "sales_2"])
    def test_sales_non_contact_do_not_see_contract(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get(f"/contracts/{4 - int(user.split('_')[-1])}/")
        assert response.status_code == 404
