import pytest
from copy import deepcopy
from utils.prettyprints import PrettifyPutReport, PRR


@pytest.mark.django_db
class TestContractUpdate:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2", "admin_1"])
    def test_contact_update_contract(self, api_client, logins, user):
        logs = getattr(logins, user)
        api_client.login(**logs)
        response = api_client.get('/contracts/')
        data = response.data[0]
        assert data["amount"] != 156331
        expected = deepcopy(data)
        data["amount"] = 156331.
        print(f"\n Trying to change first listed contract's amount: ", end='')
        url = f"/contracts/{int(user.split('_')[-1]) * 2 - 1}/"
        response = api_client.put(url, data=data)

        if user == "sales_1":
            request_dict = {'body': data, 'url': url, 'logs': logs}
            report = PrettifyPutReport(request_dict, response.data, expected)
            PRR.save_report(report.report, "change", model="contracts",
                            mode='w')
            print(f"and comparing updated contract with expected result: ", end='')
            assert "0 key error" in report.report[-1]
            assert "0 value error" in report.report[-1]

        assert response.status_code == 200
        assert response.data["amount"] == 156331

    @pytest.mark.parametrize("user", ["sales_2", "support_1", "support_2", "visitor_1"])
    def test_unauthorized_do_not_update_contracts(self, api_client, logins, user):
        api_client.login(**logins.admin_1)
        response = api_client.get('/contracts/')
        data = response.data[0]
        assert data["amount"] != 156331
        data["amount"] = 156331
        api_client.logout()
        api_client.login(**getattr(logins, user))
        response = api_client.put('/contracts/1/', data=data)
        print(f"\n Trying to change first listed contract's amount: ", end='')
        assert response.status_code in [403, 404]
