import pytest


@pytest.mark.django_db
class TestEventSearch:
    @pytest.mark.parametrize("key, value", [("client__emai", "first@client.co"),
                                            ("client__last_name", "client"),
                                            ("client__emaill__icontains", "first@clie"),
                                            ("client__last_namel__icontains", "clien"),
                                            ])
    def test_search_events_by(self, api_client, logins, key, value):
        api_client.login(**logins.sales_1)
        response = api_client.get(f'/events/?{key}={value}')
        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.parametrize("key, value", [("client__email", "first@claent.co"),
                                            ("client__last_name", "rarg"),
                                            ("client__email__icontains", "first@client.o"),
                                            ("client__last_name__icontains", "clieno"),
                                            ])
    def test_search_events_no_result(self, api_client, logins, key, value):
        api_client.login(**logins.sales_1)
        response = api_client.get(f'/events/?{key}={value}')
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_search_events_by_(self, api_client, logins):
        api_client.login(**logins.sales_1)
        response = api_client.get('/events/?client__email=first@client.co&client__last_name=client&amount=10')
        assert response.status_code == 200
        assert len(response.data) >= 1
