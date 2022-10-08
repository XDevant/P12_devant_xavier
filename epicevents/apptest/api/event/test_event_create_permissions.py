import pytest
from copy import deepcopy
from apptest.forms import event_form, expected_event
from utils.prettyprints import PrettifyReport, Report


@pytest.fixture
def data():
    form = deepcopy(event_form)
    return form


@pytest.fixture
def expected():
    expected_dict = deepcopy(expected_event)
    return expected_dict


@pytest.mark.django_db
class TestEventCreation:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2"])
    def test_sales_create_event(self, api_client, logins, user, data, expected):
        url = '/events/'
        logs = getattr(logins, user)
        api_client.login(**logs)
        data["status"] = int(user.split('_')[-1]) * 2
        expected["id"] = int(user.split('_')[-1]) + 2
        expected["client_id"] = int(user.split('_')[-1])
        response = api_client.post(url, data=data)
        assert response.status_code == 201
        if user == "sales_1":
            report = Report(url=url,
                            logs=logs,
                            action="add",
                            request_body=data,
                            expected=expected,
                            response_body=response.data,
                            mapping=(0, 0))
            pretty_report = PrettifyReport(report)
            pretty_report.save(model="events", mode='w')
            print(f"\nComparing updated event with expected result. ", end='')
            assert "0 key error" in pretty_report.errors
            assert "0 value error" in pretty_report.errors
        assert len(response.data) == 8

    @pytest.mark.parametrize("user",
                             ["sales_2", "support_1", "support_2",
                              "admin_1", "visitor_1"])
    def test_unauthorized_do_not_create_event(self,
                                              api_client,
                                              logins,
                                              user,
                                              data):
        api_client.login(**getattr(logins, user))
        data["status"] = 2
        response = api_client.post('/events/', data=data)
        print(f"\nTrying to create event without being sales contact. ",
              end='')
        assert response.status_code in [400, 403]

    @pytest.mark.parametrize("user", ["sales_1", "sales_2"])
    def test_contract_can_not_have_second_event(self,
                                                api_client,
                                                logins,
                                                user,
                                                data):
        api_client.login(**getattr(logins, user))
        resp_status = [1, 3]
        data["status"] = resp_status[int(user.split('_')[-1]) - 1]
        response = api_client.post('/events/', data=data)
        print(f"\nTrying to create second event for same contract. ",
              end='')
        assert response.status_code == 400
