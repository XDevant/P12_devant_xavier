import pytest
from copy import deepcopy
from utils.prettyprints import Report


@pytest.mark.django_db
class TestClientUpdate:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2", "admin_1"])
    def test_contact_update_client(self, api_client, logins, user):
        url = f"/clients/{int(user.split('_')[-1])}/"
        logs = getattr(logins, user)
        api_client.login(**logs)
        response = api_client.get('/clients/')
        assert '0123456789' not in response.data[0]
        data = response.data[0]
        expected = deepcopy(data)
        data["phone"] = "0123456789"
        print("\n Changing first listed client's phone number to 0123456789 ",
              end='')
        response = api_client.put(url, data=data)

        if user == "sales_1":
            report = Report(url=url,
                            logs=logs,
                            action="change",
                            request_body=data,
                            expected=expected,
                            response_body=response.data)
            report.save(model="clients", mode='w')
            print("and comparing updated client with expected result: ",
                  end='')
            assert "0 key error" in report.errors
            assert "0 value error" in report.errors

        assert response.status_code == 200
        assert '0123456789' in response.data["phone"]

    @pytest.mark.parametrize("user", ["sales_2",
                                      "support_1",
                                      "support_2",
                                      "visitor_1"])
    def test_unauthorized_do_not_update_clients(self,
                                                api_client,
                                                logins,
                                                user):
        api_client.login(**logins.sales_1)
        response = api_client.get('/clients/')
        data = response.data[0]
        data["phone"] = "0123456789"
        api_client.logout()
        api_client.login(**getattr(logins, user))
        response = api_client.put('/clients/1/', data=data)
        print("\n Trying to change first listed client's phone number: ",
              end='')
        assert response.status_code in [403, 404]
