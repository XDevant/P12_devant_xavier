import pytest
from utils.prettyprints import PrettifyReport, Report


@pytest.mark.django_db
class TestClientSearch:
    @pytest.mark.parametrize("key, value", [("email", "first@client.co"),
                                            ("last_name", "client"),
                                            ("email__icontains", "first@client"),
                                            ("last_name__icontains", "clien")])
    def test_search_clients_by(self, api_client, logins, key, value):
        url = f'/clients/?{key}={value}'
        logs = logins.sales_1
        api_client.login(**logs)
        response = api_client.get(url)
        report = Report(url=url,
                        logs=logs,
                        action="search",
                        response_body=response.data)
        pretty_report = PrettifyReport(report)
        mode = 'a'
        if key == "email":
            mode = 'w'
        pretty_report.save(model="clients", mode=mode)
        assert response.status_code == 200
        assert len(response.data) >= 1

    @pytest.mark.parametrize("key, value", [("email", "first@claent.co"),
                                            ("last_name", "rarg"),
                                            ("email__icontains", "first@client.cat"),
                                            ("last_name__icontains", "clients")])
    def test_search_clients_no_result(self, api_client, logins, key, value):
        api_client.login(**logins.sales_1)
        response = api_client.get(f'/clients/?{key}={value}')
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_search_clients_by_both(self, api_client, logins):
        api_client.login(**logins.sales_1)
        response = api_client.get(f'/clients/?email=first@client.co&last_name=client')
        assert response.status_code == 200
        assert len(response.data) >= 1
