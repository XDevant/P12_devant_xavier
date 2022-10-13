import pytest
from utils.prettyprints import Report


@pytest.mark.django_db
class TestContractSearch:
    @pytest.mark.parametrize("key, value",
                             [("client__email", "first@client.co"),
                              ("client__last_name", "Client"),
                              ("client__email__icontains", "first@client"),
                              ("client__last_name__icontains", "Clien"),
                              ("amount", "1000"),
                              ("amount__gt", "25000"),
                              ("amount__lt", "25000"),
                              ("date_created__lt", "2040-09-10T00:00:00Z"),
                              ("date_created__gt", "2010-09-10T00:00:00Z")
                              ])
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
        mode = 'a'
        if key == "client__email":
            mode = 'w'
        report.save(model="contracts", mode=mode)
        if "date_created" not in key:
            assert 1 <= len(response.data) <= 2
        else:
            assert len(response.data) == 4

    @pytest.mark.parametrize("key, value",
                             [("client__email", "first@claent.co"),
                              ("client__last_name", "rarg"),
                              ("client__email__icontains", "first@client.o"),
                              ("client__last_name__icontains", "clieno"),
                              ("amount", "9"),
                              ("date_created__lt", "2010-09-10T00:00:00Z")
                              ])
    def test_search_contracts_no_result(self, api_client, logins, key, value):
        api_client.login(**logins.sales_1)
        response = api_client.get(f'/contracts/?{key}={value}')
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_search_contracts_by_both(self, api_client, logins):
        api_client.login(**logins.sales_1)
        url = '/contracts/?client__email=first@client.co'
        url += '&client__last_name=Client&amount=1000'
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) >= 1
