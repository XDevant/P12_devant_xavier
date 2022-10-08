import pytest
from datetime import date, timedelta
from utils.prettyprints import PrettifyReport, Report


@pytest.mark.django_db
class TestEventSearch:
    @pytest.mark.parametrize("key, value",
                             [("client__email", "first@client.co"),
                              ("client__last_name", "Client"),
                              ("client__email__icontains", "first@client"),
                              ("client__last_name__icontains", "Clien"),
                              ("date_created__lt", "2040-09-10T00:00:00Z"),
                              ("date_created__gt", "2010-09-10T00:00:00Z")])
    def test_search_events_by(self, api_client, logins, key, value):
        logs = logins.sales_1
        url = f'/events/?{key}={value}'
        api_client.login(**logs)
        response = api_client.get(url)
        assert response.status_code == 200
        report = Report(url=url,
                        logs=logs,
                        action="search",
                        response_body=response.data)
        pretty_report = PrettifyReport(report)
        mode = 'a'
        if key == "client__email":
            mode = 'w'
        pretty_report.save(model="events", mode=mode)
        if "date_created" not in key:
            assert len(response.data) == 1
        else:
            assert len(response.data) == 2

    @pytest.mark.parametrize("key, value",
                             [("client__email", "first@claent.co"),
                              ("client__last_name", "rarg"),
                              ("client__email__icontains", "first@client.o"),
                              ("client__last_name__icontains", "clieno"),
                              ("date_created__lt", "2010-09-10T00:00:00Z")])
    def test_search_events_no_result(self, api_client, logins, key, value):
        api_client.login(**logins.sales_1)
        response = api_client.get(f'/events/?{key}={value}')
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_search_events_by_both(self, api_client, logins):
        api_client.login(**logins.sales_1)
        url = '/events/?client__email=first@client.co'
        url += '&client__last_name=Client&amount=1000'
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) >= 1
