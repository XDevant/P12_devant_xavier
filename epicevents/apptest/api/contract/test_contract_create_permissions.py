import pytest
from copy import deepcopy
from apptest.forms import contract_form, expected_contract
from utils.prettyprints import PrettifyPostReport, PRR


@pytest.fixture
def data():
    form = deepcopy(contract_form)
    return form


@pytest.fixture
def expected():
    expected_dict = deepcopy(expected_contract)
    return expected_dict


@pytest.mark.django_db
class TestContractCreation:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2"])
    def test_sales_create_contract(self,
                                   api_client,
                                   logins,
                                   user,
                                   data,
                                   expected):
        logs = getattr(logins, user)
        api_client.login(**logs)
        data["client_id"] = int(user.split('_')[-1])
        response = api_client.post('/contracts/', data=data)

        if user == "sales_1":
            request_dict = {'body': data, 'url': '/contracts/', 'logs': logs}
            report = PrettifyPostReport(request_dict,
                                        response.data,
                                        expected,
                                        [0, 1])
            PRR.save_report(report.report, "add", model="contracts", mode='w')
            assert "0 key error" in report.report[-1]
            assert "0 value error" in report.report[-1]

        assert response.status_code == 201
        assert logs["email"] in response.data["contact"]

    @pytest.mark.parametrize(
        "user", ["support_1", "support_2", "admin_1", "visitor_1"])
    def test_unauthorized_do_not_create_contract(self,
                                                 api_client,
                                                 logins,
                                                 user,
                                                 data):
        api_client.login(**getattr(logins, user))
        data["client_id"] = 1
        response = api_client.post('/contracts/', data=data)
        assert response.status_code >= 400

    @pytest.mark.parametrize("user", ["sales_1", "sales_2"])
    def test_sales_do_not_create_contract_for_wrong_client(self,
                                                           api_client,
                                                           logins,
                                                           user,
                                                           data):
        api_client.login(**getattr(logins, user))
        data["client_id"] = int(user.split('_')[-1]) % 2 + 1
        response = api_client.post('/contracts/', data=data)
        assert response.status_code == 400
