from rest_framework.test import APITestCase
import pytest


user_logs = [
        ("de@de.co", "mdp1"),
        ("do@do.co", "mdp2"),
        ("bi@bi.co", "mdp3"),
        ("bo@bo.co", "mdp4"),
        ("za@za.co", "mdp5"),
        ("zo@zo.co", "mdp6"),
    ]


@pytest.mark.django_db
class TestClientRead:
    @pytest.mark.parametrize("users,expected", [pytest.param(user_logs[i], 200) for i in range(5)])
    def test_contact_see_clients(self, api_client, users, expected):
        username, password = users
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/clients/')
        assert response.status_code == expected

    def test_unauthorized_do_not_see_clients(self, api_client):
        username, password = user_logs[5]
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/clients/')
        assert response.status_code in [204, 403]

    @pytest.mark.parametrize("user", [pytest.param(user_logs[i],) for i in range(0, 6, 2)])
    def test_contact_see_client_1(self, api_client, user):
        username, password = user
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/clients/1/')
        assert response.status_code == 200

    @pytest.mark.parametrize("user", [pytest.param(user_logs[i], ) for i in range(1, 6, 2)])
    def test_non_contact_do_not_see_client_1(self, api_client, user):
        username, password = user
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/clients/1/')
        assert response.status_code in [204, 403, 404]

    @pytest.mark.parametrize("user", [pytest.param(user_logs[i], ) for i in [1, 3, 4]])
    def test_contact_see_client_2(self, api_client, user):
        username, password = user
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/clients/2/')
        assert response.status_code == 200

    @pytest.mark.parametrize("user", [pytest.param(user_logs[i], ) for i in [0, 2, 5]])
    def test_non_contact_do_not_see_client_1(self, api_client, user):
        username, password = user
        api_client.login(username=username, password=password)
        response = api_client.get('http://127.0.0.1:8000/clients/2/')
        assert response.status_code in [204, 403, 404]




