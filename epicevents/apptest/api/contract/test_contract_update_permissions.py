import pytest
from copy import deepcopy
from utils.prettyprints import Report


@pytest.mark.django_db
class TestContractUpdate:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2", "admin_1"])
    def test_contact_update_contract(self, api_client, logins, user):
        url = f"/contracts/{int(user.split('_')[-1]) * 2 - 1}/"
        logs = getattr(logins, user)
        api_client.login(**logs)
        expected = api_client.get(url).data
        assert expected != 156331
        data = {"amount": 156331.,
                "payment_due": expected["payment_due"]}
        print("\n Trying to change first listed contract's amount: ", end='')
        url = f"/contracts/{int(user.split('_')[-1]) * 2 - 1}/"
        response = api_client.put(url, data=data)
        assert response.status_code == 200

        if user == "sales_1":
            report = Report(url=url,
                            logs=logs,
                            action="change",
                            request_body=data,
                            expected=expected,
                            response_body=response.data)
            report.save(model="contracts", mode='w')
            print("and comparing updated contract with expected result: ",
                  end='')
            assert "0 key error" in report.errors
            assert "0 value error" in report.errors
        assert response.data["amount"] == 156331

    @pytest.mark.parametrize("user", ["sales_2",
                                      "support_1",
                                      "support_2",
                                      "visitor_1"])
    def test_unauthorized_do_not_update_contracts(self,
                                                  api_client,
                                                  logins,
                                                  user):
        api_client.login(**logins.admin_1)
        url = '/contracts/1/'
        expected = api_client.get(url).data
        assert expected["amount"] != 156331
        data = {"amount": 156331.,
                "payment_due": expected["payment_due"]}
        api_client.logout()
        api_client.login(**getattr(logins, user))
        response = api_client.put(url, data=data)
        print("\n Trying to change first listed contract's amount: ", end='')
        assert response.status_code in [403, 404]
