import pytest

data = {
                "first_name":  "third",
                "last_name":  "client",
                "email":  "third@client.co",
                "phone":  "01",
                "mobile":  "08",
                "company_name":  "World"
        }


@pytest.mark.django_db
class TestClientCreation:
    @pytest.mark.parametrize("user", ["sales_1", "sales_2"])
    def test_sales_create_client(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.post('/clients/', data=data)
        assert response.status_code == 201

    @pytest.mark.parametrize("user", ["support_1", "support_2", "admin_1", "visitor_1"])
    def test_unauthorized_do_not_create_client(self, api_client, logins, user):
        api_client.login(**getattr(logins, user))
        response = api_client.post('/clients/', data=data)
        assert response.status_code == 403
