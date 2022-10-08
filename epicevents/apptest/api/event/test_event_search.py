import pytest
from datetime import date, timedelta, datetime
from utils.prettyprints import PrettifyReport, Report


@pytest.mark.django_db
class TestEventSearch:
    @pytest.mark.parametrize("key, value",
                             [("client__email", "first@client.co"),
                              ("client__last_name", "client"),
                              ("client__email__icontains", "first@client"),
                              ("client__last_name__icontains", "clien"),
                              ("date_created__lt", str(datetime.now())),
                              ("date_created__gt",
                               str(date.today() - timedelta(days=15000)))])
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
        assert len(response.data) == 1

    @pytest.mark.parametrize("key, value",
                             [("client__email", "first@claent.co"),
                              ("client__last_name", "rarg"),
                              ("client__email__icontains", "first@client.o"),
                              ("client__last_name__icontains", "clieno"),
                              ("date_created__gt",
                               str(date.today() + timedelta(days=1)))])
    def test_search_events_no_result(self, api_client, logins, key, value):
        api_client.login(**logins.sales_1)
        response = api_client.get(f'/events/?{key}={value}')
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_search_events_by_(self, api_client, logins):
        api_client.login(**logins.sales_1)
        url = '/events/?client__email=first@client.co'
        url += '&client__last_name=client&amount=10'
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) >= 1
