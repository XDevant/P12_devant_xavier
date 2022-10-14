import pytest
from copy import deepcopy
from utils.prettyprints import Report
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
        url = '/contracts/'
        logs = getattr(logins, user)
        api_client.login(**logs)
        response = api_client.get(url)
        kvs = expected.items()
        expected = {k if k != "client" else "client_id": v for k, v in kvs}

        if user == "sales_1":
            report = Report(url=url,
                            logs=logs,
                            action="list",
                            response_body=response.data)
            report.save(model="contracts", mode='w')
            report = Report(url=url,
                            logs=logs,
                            action="list",
                            expected=expected,
                            response_body=response.data)
            assert "0 key error" in report.errors
            assert "0 value error" in report.errors

        assert response.status_code == 200
        if user != "admin_1":
            assert len(response.data) == 4
        else:
            assert len(response.data) == 8

    @pytest.mark.parametrize("user", ["support_1", "support_2", "visitor_1"])
    def test_unauthorized_do_not_see_contracts(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/contracts/')
        assert response.status_code == 403

    @pytest.mark.parametrize("user", ["sales_1", "sales_2", "admin_1"])
    def test_sales_i_see_contract_i(self, api_client, logins, user, expected):
        url = f"/contracts/{int(user.split('_')[-1]) * 2 - 1}/"
        logs = getattr(logins, user)
        api_client.login(**logs)
        response = api_client.get(url)
        expected["date_updated"] = None

        if user == "sales_1":
            report = Report(url=url,
                            logs=logs,
                            action="detail",
                            expected=expected,
                            response_body=response.data)
            report.save(model="contracts", mode='w')
            assert "0 key error" in report.errors
            assert "0 value error" in report.errors

        assert response.status_code == 200
        assert len(response.data) == 8

    @pytest.mark.parametrize("user", ["support_1", "support_2", "visitor_1"])
    def test_non_sales_do_not_see_contract_1(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.get('/contracts/1/')
        assert response.status_code in [403, 404]

    @pytest.mark.parametrize("user", ["sales_1", "sales_2"])
    def test_sales_non_contact_do_not_see_contract(self,
                                                   api_client,
                                                   logins,
                                                   user):
        api_client.login(**getattr(logins, user))
        url = f"/contracts/{4 - int(user.split('_')[-1])}/"
        response = api_client.get(url)
        assert response.status_code == 404
