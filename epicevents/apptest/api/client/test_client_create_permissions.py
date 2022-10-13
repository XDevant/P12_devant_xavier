import pytest
from copy import deepcopy
from apptest.forms import client_form, expected_client
from utils.prettyprints import Report


@pytest.fixture
def data():
    form = deepcopy(client_form)
    return form


@pytest.fixture
def expected():
    expected_dict = deepcopy(expected_client)
    return expected_dict


@pytest.mark.django_db
class TestClientCreation:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2"])
    def test_sales_create_client(self,
                                 api_client,
                                 logins,
                                 user,
                                 data,
                                 expected):
        url = '/clients/'
        logs = getattr(logins, user)
        api_client.login(**logs)
        response = api_client.post(url, data=data)
        if user == "sales_1":
            report = Report(url=url,
                            logs=logs,
                            action="add",
                            request_body=data,
                            expected=expected,
                            response_body=response.data,
                            mapping=(0, 0))
            report.save(model="clients", mode='w')
            assert "0 key error" in report.errors
            assert "0 value error" in report.errors
        assert response.status_code == 201

    @pytest.mark.parametrize("user", ["support_1",
                                      "support_2",
                                      "admin_1",
                                      "visitor_1"])
    def test_unauthorized_do_not_create_client(self,
                                               api_client,
                                               logins,
                                               user,
                                               data):
        api_client.login(**getattr(logins, user))
        response = api_client.post('/clients/', data=data)
        assert response.status_code == 403
