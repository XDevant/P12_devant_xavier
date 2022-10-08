import pytest
from datetime import date, timedelta
from utils.prettyprints import PrettifyReport, Report


@pytest.mark.django_db
class TestContractSearch:
    @pytest.mark.parametrize("key, value", [("client__email", "first@client.co"),
                                            ("client__last_name", "client"),
                                            ("client__email__icontains", "first@client"),
                                            ("client__last_name__icontains", "clien"),
                                            ("amount", "10"),
                                            ("amount__gt", "9"),
                                            ("amount__lt", "99"),
                                            ("date_created__lt", str(date.today() + timedelta(days=1))),
                                            ("date_created__gt", str(date.today() - timedelta(days=15000)))])
    def test_search_contracts_by(self, api_client, logins, key, value):
        url = f'/contracts/?{key}={value}'
        logs = logins.sales_1
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
        pretty_report.save(model="contracts", mode=mode)
        assert 1 <= len(response.data) <= 2

    @pytest.mark.parametrize("key, value", [("client__email", "first@claent.co"),
                                            ("client__last_name", "rarg"),
                                            ("client__email__icontains", "first@client.o"),
                                            ("client__last_name__icontains", "clieno"),
                                            ("amount", "9"),
                                            ("date_created__gt", date.today() + timedelta(days=15))])
    def test_search_contracts_no_result(self, api_client, logins, key, value):
        api_client.login(**logins.sales_1)
        response = api_client.get(f'/contracts/?{key}={value}')
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_search_contracts_by_(self, api_client, logins):
        api_client.login(**logins.sales_1)
        response = api_client.get('/contracts/?client__email=first@client.co&client__last_name=client&amount=10')
        assert response.status_code == 200
        assert len(response.data) >= 1
